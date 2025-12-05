# MVP 3: Statistics & Insights Plan

## Objective
Transform raw frame-by-frame analysis data into actionable insights.
We will generate two forms of statistics for each analyzed video:
1.  **Human-Readable Report (`summary_report.txt`)**: A text file summarizing the emotional content.
2.  **Machine-Readable Data (`statistics.json`)**: A structured JSON file containing calculated metrics for future use (e.g., dashboards).

## Features
1.  **Statistics Calculation**:
    *   Calculate **Overall Dominant Emotion** (the emotion that appears most frequently).
    *   Calculate **Emotion Distribution** (percentage of frames for each emotion).
    *   Identify **Peaks** (timestamps where specific emotions had the highest confidence scores).
2.  **Report Generation**:
    *   Generate a formatted text report.
    *   Generate a JSON data file.

## Architecture Design

We will introduce a new `statistics` module in the `core` layer and a `reporting` module in the `infrastructure` layer.

### 1. Domain Models (`backend/src/core/domain.py` or new `stats.py`)
We need a data structure to hold the calculated statistics, independent of how they are displayed.

```python
@dataclass
class VideoStatistics:
    video_name: str
    total_frames: int
    duration_seconds: float
    dominant_emotion: str
    emotion_distribution: Dict[str, float]  # e.g., {"happy": 45.5, "sad": 10.0}
    peaks: Dict[str, Tuple[str, float]]     # e.g., {"happy": ("00:01:15", 0.98)}
```

### 2. Statistics Calculator (`backend/src/core/statistics.py`)
A service class responsible for processing a list of `Frame` objects and producing a `VideoStatistics` object.

```python
class StatisticsCalculator:
    def calculate(self, video_name: str, frames: List[Frame]) -> VideoStatistics:
        # Logic to compute averages, counts, and max scores
        pass
```

### 3. Reporting Interface (`backend/src/core/interfaces.py`)
An interface to allow different types of reports.

```python
class IReporter(ABC):
    @abstractmethod
    def generate(self, stats: VideoStatistics, output_dir: str) -> None:
        pass
```

### 4. Infrastructure Implementations (`backend/src/infrastructure/reporting.py`)
Concrete implementations of the reporter.

*   `TextReporter`: Writes `summary_report.txt`.
*   `JsonReporter`: Writes `statistics.json`.

## Implementation Steps

1.  **Define Data Structures**: Create `VideoStatistics` dataclass.
2.  **Implement Calculator**: Create `StatisticsCalculator` to compute the math.
3.  **Implement Reporters**: Create `TextReporter` and `JsonReporter`.
4.  **Integrate**: Update `Analyzer` or `CLI` to:
    *   Run the analysis (existing).
    *   Pass results to `StatisticsCalculator`.
    *   Pass `VideoStatistics` to the reporters.
5.  **Update CLI**: Ensure the output directory structure supports these new files (e.g., `data/output/<video_name>/`).

## Output Structure
```
data/output/
└── MarkRutte_MariekeElsinga/
    ├── analysis.csv          (Existing MVP 2)
    ├── summary_report.txt    (New MVP 3)
    └── statistics.json       (New MVP 3)
```
