#include <iostream>
#include <fstream>
#include <sstream>
#include <string>
#include <vector>
#include <filesystem>
#include <cstdlib>
#include <array>
#include <stdexcept>
#include <openssl/evp.h> // For modern hashing

namespace fs = std::filesystem;

// Function to compute the SHA256 hash of a file

std::string hash_file(const std::string &file_path) {
    std::ifstream file(file_path, std::ios::binary);
    if (!file.is_open()) {
        throw std::runtime_error("Could not open file: " + file_path);
    }

    EVP_MD_CTX *ctx = EVP_MD_CTX_new();
    if (!ctx) {
        throw std::runtime_error("Failed to create EVP_MD_CTX");
    }

    if (EVP_DigestInit_ex(ctx, EVP_sha256(), nullptr) != 1) {
        EVP_MD_CTX_free(ctx);
        throw std::runtime_error("Failed to initialize digest");
    }

    char buffer[4096];
    while (file.read(buffer, sizeof(buffer))) {
        if (EVP_DigestUpdate(ctx, buffer, file.gcount()) != 1) {
            EVP_MD_CTX_free(ctx);
            throw std::runtime_error("Failed to update digest");
        }
    }

    if (file.gcount() > 0) {
        if (EVP_DigestUpdate(ctx, buffer, file.gcount()) != 1) {
            EVP_MD_CTX_free(ctx);
            throw std::runtime_error("Failed to update digest");
        }
    }

    unsigned char hash[EVP_MAX_MD_SIZE];
    unsigned int hash_len;
    if (EVP_DigestFinal_ex(ctx, hash, &hash_len) != 1) {
        EVP_MD_CTX_free(ctx);
        throw std::runtime_error("Failed to finalize digest");
    }

    EVP_MD_CTX_free(ctx);

    std::ostringstream result;
    for (unsigned int i = 0; i < hash_len; ++i) {
        result << std::hex << std::setw(2) << std::setfill('0') << (int)hash[i];
    }
    return result.str();
}


// Function to run shell commands and capture output
std::string run_command(const std::string &command) {
    std::array<char, 128> buffer;
    std::string result;
    std::shared_ptr<FILE> pipe(popen(command.c_str(), "r"), pclose);
    if (!pipe) throw std::runtime_error("popen() failed!");

    while (fgets(buffer.data(), buffer.size(), pipe.get()) != nullptr) {
        result += buffer.data();
    }
    return result;
}

// Function to download datasets from Kaggle
void download_datasets(const std::string &search_term, const std::string &dest_folder, const std::string &sort_by = "hottest", int page_limit = 5) {
    // Ensure the destination folder exists
    fs::create_directories(dest_folder);

    for (int page = 1; page <= page_limit; ++page) {
        std::cout << "Fetching page " << page << " for datasets..." << std::endl;

        try {
            // Construct Kaggle CLI command for fetching datasets
            std::string command = "kaggle datasets list -s \"" + search_term + "\" -p " + std::to_string(page) + " --sort-by " + sort_by;
            std::string output = run_command(command);

            std::istringstream iss(output);
            std::string line;
            while (std::getline(iss, line)) {
                if (line.find("/") == std::string::npos) continue; // Skip irrelevant lines

                std::string dataset_ref = line.substr(0, line.find(" "));
                std::string dataset_name = dataset_ref.substr(dataset_ref.find("/") + 1);

                std::string dataset_folder = dest_folder + "/" + dataset_name;
                if (fs::exists(dataset_folder)) {
                    std::cout << "Dataset '" << dataset_name << "' already downloaded, skipping..." << std::endl;
                    continue;
                }

                std::cout << "Downloading dataset: " << dataset_name << "..." << std::endl;
                try {
                    // Construct Kaggle CLI command for downloading datasets
                    std::string download_command = "kaggle datasets download -d " + dataset_ref + " -p " + dest_folder + " --unzip";
                    run_command(download_command);
                    std::cout << "Successfully downloaded and extracted '" << dataset_name << "'." << std::endl;
                } catch (const std::exception &e) {
                    std::cerr << "Error downloading '" << dataset_name << "': " << e.what() << std::endl;
                }
            }
        } catch (const std::exception &e) {
            std::cerr << "Error fetching datasets on page " << page << ": " << e.what() << std::endl;
            break;
        }
    }
}

int main() {
    const std::string SEARCH_TERM = "Predictive Maintenance Dataset";
    const std::string DESTINATION_FOLDER = "data/raw/kaggle_datasets";
    const std::string SORT_ORDER = "hottest"; // Options: newest, oldest, hottest, etc.
    const int PAGE_LIMIT = 6;

    try {
        download_datasets(SEARCH_TERM, DESTINATION_FOLDER, SORT_ORDER, PAGE_LIMIT);
    } catch (const std::exception &e) {
        std::cerr << "An error occurred: " << e.what() << std::endl;
    }

    return 0;
}
