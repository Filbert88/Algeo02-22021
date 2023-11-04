use actix_multipart::Multipart;
use actix_web::{web, App, Error, HttpServer, HttpResponse, Responder};
use futures::{StreamExt, TryStreamExt};
use std::io::Write;
use serde::{Serialize, Deserialize};
use std::sync::Mutex;
use env_logger::Env;
use log::{info, error};

#[derive(Serialize, Clone)]
struct Item {
    id: u32,
    name: String,
}

struct AppState {
    items: Vec<Item>,
    current_page : Mutex<i32>
}

#[derive(Deserialize)]
struct Action {
    direction: String,
}

#[actix_web::main]
async fn main() -> std::io::Result<()> {
    let app_data = web::Data::new(AppState {
        items: (1..=100).map(|i| Item { id: i, name: format!("Item {}", i) }).collect(),
        current_page: Mutex::new(-1)
    });

    env_logger::Builder::from_env(Env::default().default_filter_or("info")).init();
    info!("Starting the server at http://127.0.0.1:8080/");
    HttpServer::new(move || {
        App::new()
            .app_data(app_data.clone())
            .route("/", web::get().to(index))
            .route("/items", web::post().to(paginated_items))
            .route("/upload", web::post().to(upload))
    })
    .bind(("127.0.0.1", 8080))?
    .run()
    .await
}

const PAGE_SIZE: usize = 10;

fn paginate(items: &[Item], page: usize) -> Vec<Item> {
    let start = page * PAGE_SIZE;
    let end = start + PAGE_SIZE;
    items.get(start..end).unwrap_or(&[]).to_vec()
}

async fn paginated_items(data: web::Data<AppState>, action: web::Form<Action>) -> impl Responder {
    let mut page = match data.current_page.lock() {
        Ok(guard) => guard,
        Err(e) => {
            error!("Failed to acquire lock on current_page: {}", e);
            return HttpResponse::InternalServerError().finish();
        }
    };
    match action.direction.as_str() {
        "next" => *page += 1,
        "prev" => *page -= 1,
        _ => (),
    }
    let total_items = data.items.len();
    let total_pages = (total_items + PAGE_SIZE - 1) / PAGE_SIZE;
    let items = paginate(&data.items, (*page).try_into().unwrap());
    info!("Serving paginated items for page {}", *page);
    
    // Generate the HTML for the paginated items
    let items_html = items.iter().map(|item| {
        format!("<div>{}: {}</div>", item.id, item.name)
    }).collect::<String>();

    // Generate the HTML for the pagination controls
    let prev_button_html = if *page == 0 as i32 {
        r#"<button disabled>Previous</button>"#.to_string()
    } else {
        r#"<button hx-post="/items" hx-target='#items-list' hx-vals='{"direction": "prev"}' hx-swap="innerHTML">Previous</button>"#.to_string()
    };

    let next_button_html = if *page == (total_pages as i32) - 1 {
        r#"<button disabled>Next</button>"#.to_string()
    } else {
        r#"<button hx-post="/items" hx-target='#items-list' hx-vals='{"direction": "next"}' hx-swap="innerHTML">Next</button>"#.to_string()
    };

    // Combine the items and buttons into one HTML snippet
    let full_html = format!(
        "{}<nav id='pagination-controls'>{}</nav>",
        items_html,
        format!("{}{}", prev_button_html, next_button_html)
    );

    HttpResponse::Ok().content_type("text/html").body(full_html)
}

async fn index(data: web::Data<AppState>) -> impl Responder {
    let mut page = data.current_page.lock().unwrap();
    *page = -1;
    info!("Reset pagination and serving index.html");
    HttpResponse::Ok().content_type("text/html").body(include_str!("../static/index.html"))
}

async fn upload(mut payload: Multipart) -> Result<HttpResponse, Error> {
    // Iterate over multipart stream
    let mut image_name = String::new();
    while let Ok(Some(mut field)) = payload.try_next().await {
        let content_disposition = field.content_disposition();
        let filename = content_disposition.get_filename().unwrap();
        image_name = filename.to_string();
        let filepath = format!("./images/{}", sanitize_filename::sanitize(&filename));

        // File::create is blocking operation, use threadpool
        let mut f = web::block(|| std::fs::File::create(filepath))
            .await
            .unwrap();

        // Field in turn is stream of *Bytes* object
        while let Some(chunk) = field.next().await {
            let data = chunk.unwrap();
            // filesystem operations are blocking, we have to use threadpool
            f = web::block(move || f.as_ref().expect("REASON").write_all(&data).map(|_| f))
                .await
                .map_err(|e| {
                    error!("File write error: {}", e);
                    actix_web::error::ErrorInternalServerError(e)
                })??;
        }
    }
    let image_url = format!("/images/{}", sanitize_filename::sanitize(&image_name.as_str()));
    Ok(HttpResponse::Ok()
        .content_type("text/html")
        .body(format!("<img src='{}' alt='Uploaded Image'/><p>Uploaded Image</p>",image_url))
    )
}