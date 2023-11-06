use std::env;
use std::error::Error;
use std::fs;
use std::path::{PathBuf};
use zip_extensions::*;
use zip::ZipArchive;

fn main() -> Result<(), Box<dyn Error>> {
    let args: Vec<String> = env::args().collect();
    let zip_file_path = &args[1];
    let output_dir = &args[2];
    let archive_file: PathBuf = PathBuf::from(zip_file_path);
    let mut target_dir: PathBuf = PathBuf::from(output_dir);
    let dataset_dir: PathBuf = PathBuf::from(output_dir).join("dataset");
    fs::remove_dir_all(&dataset_dir)?;
    fs::create_dir_all(&target_dir)?;
    zip_extract(&archive_file, &target_dir)?;
    let file = std::fs::File::open(zip_file_path)?;
    let mut archive = ZipArchive::new(file)?;
    let binding = archive.by_index(0)?;
    let extracted_folder_name = binding.name().split('/').next().unwrap_or("");
    let temp_extracted_dir = target_dir.join(extracted_folder_name);
    target_dir = PathBuf::from(output_dir).join("dataset");
    fs::rename(&temp_extracted_dir, &target_dir)?;
    Ok(())
}
