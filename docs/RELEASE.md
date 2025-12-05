# Release Notes

## v0.1.0 - MVP 1: Core Proof of Concept

**Release Date:** December 4, 2025

This is the initial release of the **TV Show Emotion Analyzer**, focusing on establishing the core architecture and proving the feasibility of AI-based emotion detection.

### 🚀 New Features

-   **Single Image Analysis:** The tool can now accept a single image file (JPG/PNG) and detect the dominant emotion using the DeepFace library.
-   **CLI Interface:** A command-line interface (`cli.py`) allows users to run the tool with arguments for input, output, and specific image paths.
-   **CSV Export:** Analysis results (dominant emotion + confidence scores for 7 emotions) are automatically saved to a CSV file (`analysis_results.csv`) in the specified output directory.
-   **Clean Architecture:** The codebase has been refactored to follow Clean Architecture principles:
    -   **Domain Layer:** `InputData` and `OutputData` models.
    -   **Core Layer:** `EmotionAnalyzer` (Use Case) and `Frame` (Entity).
    -   **Infrastructure Layer:** `DeepFaceAnalyzer` (AI Wrapper) and `CSVStorage` (Persistence).
    -   **Presentation Layer:** CLI adapter.
-   **Dependency Injection:** The core analyzer is decoupled from specific implementations, allowing for easier testing and future upgrades.

### 🛠 Technical Improvements

-   **Robust Logging:** Implemented a singleton-style logger that outputs to the console (extensible to files).
-   **Error Handling:** Added graceful handling for missing files, invalid paths, and "No Face Detected" scenarios.
-   **Project Structure:** Established a scalable folder structure (`backend/src/core`, `backend/src/infrastructure`, `backend/src/model`, `backend/src/presentation`).

### 🐛 Known Issues / Limitations

-   **Video Processing:** While the structure is in place, actual video frame extraction is not yet implemented (Scheduled for MVP 2).
-   **Performance:** DeepFace initialization time is noticeable for single images.
-   **Face Detection:** Currently relies on OpenCV backend; may struggle with side profiles or low-resolution faces.

### 🔜 Next Steps (MVP 2)

-   Implement `VideoProcessor` to extract frames from video files.
-   Add batch processing for multiple videos in a folder.
