# Architecture Documentation
## Swiss Weather Sport Planner

### System Overview

The Swiss Weather Sport Planner is a single-page web application built with Django that provides real-time weather-based sport recommendations for outdoor activities in Reinach BL, Switzerland.

## High-Level Architecture

```mermaid
graph TB
    User[User Browser]
    Django[Django Server]
    OpenWeather[OpenWeatherMap API]
    LocalStorage[(Local Storage)]
    
    User -->|HTTP Requests| Django
    Django -->|HTML/CSS/JS| User
    Django -->|API Requests| OpenWeather
    OpenWeather -->|Weather Data| Django
    User -->|Store Preferences| LocalStorage
    LocalStorage -->|Load Preferences| User
    
    style User fill:#e1f5ff
    style Django fill:#ffe1e1
    style OpenWeather fill:#e1ffe1
    style LocalStorage fill:#fff4e1
```

## Component Architecture

```mermaid
graph LR
    subgraph "Frontend Layer"
        UI[UI Components]
        Charts[Chart.js Visualizations]
        Prefs[Preference Manager]
        Storage[Local Storage Handler]
    end
    
    subgraph "Django Backend"
        Views[Django Views]
        Weather[Weather Service]
        Sports[Sport Recommendation Engine]
        Templates[Django Templates]
    end
    
    subgraph "External Services"
        API[OpenWeatherMap API]
    end
    
    UI --> Views
    Charts --> Views
    Prefs --> Storage
    Views --> Weather
    Views --> Sports
    Views --> Templates
    Weather --> API
    Templates --> UI
    
    style UI fill:#e1f5ff
    style Charts fill:#e1f5ff
    style Prefs fill:#e1f5ff
    style Views fill:#ffe1e1
    style Weather fill:#ffe1e1
    style Sports fill:#ffe1e1
    style API fill:#e1ffe1
```

## Data Flow Architecture

```mermaid
sequenceDiagram
    participant User
    participant Browser
    participant Django
    participant WeatherAPI as OpenWeatherMap
    participant LocalStorage
    
    User->>Browser: Visit Application
    Browser->>Django: GET /
    Django->>WeatherAPI: Request Weather Data (Reinach BL)
    WeatherAPI-->>Django: Weather Data (Current + 24h Forecast)
    
    Browser->>LocalStorage: Load User Preferences
    LocalStorage-->>Browser: Return Preferences (or defaults)
    
    Django->>Django: Calculate Sport Recommendations
    Django-->>Browser: Render HTML + Data
    Browser-->>User: Display Weather + Recommendations
    
    User->>Browser: Modify Preferences
    Browser->>LocalStorage: Save New Preferences
    Browser->>Browser: Recalculate Recommendations
    Browser-->>User: Update Display
```

## Application Layer Structure

```mermaid
graph TD
    subgraph "Presentation Layer"
        A[Single Page Application]
        B[Current Weather Display]
        C[Sport Recommendations]
        D[Temperature Chart]
        E[Rain Chart]
        F[Wind Chart]
        G[Preference Editor]
    end
    
    subgraph "Business Logic Layer"
        H[Weather Data Fetcher]
        I[Sport Recommendation Logic]
        J[Temperature Evaluator]
        K[Wind Evaluator]
        L[Rain Evaluator]
    end
    
    subgraph "Data Layer"
        M[OpenWeatherMap API Client]
        N[Preference Validator]
    end
    
    A --> B
    A --> C
    A --> D
    A --> E
    A --> F
    A --> G
    
    B --> H
    C --> I
    D --> H
    E --> H
    F --> H
    G --> N
    
    I --> J
    I --> K
    I --> L
    
    H --> M
    
    style A fill:#e1f5ff
    style I fill:#ffe1e1
    style M fill:#e1ffe1
```

## Sport Recommendation Logic Flow

```mermaid
flowchart TD
    Start[Receive Weather Data] --> LoadPrefs[Load User Preferences]
    LoadPrefs --> GetSports[Get Selected Sports]
    
    GetSports --> CheckCycling{Cycling Selected?}
    CheckCycling -->|Yes| EvalCycling[Evaluate Cycling Conditions]
    CheckCycling -->|No| CheckRunning
    
    EvalCycling --> CyclingTemp{Temperature in Range?}
    CyclingTemp -->|No| CyclingBad[❌ Cycling Not Recommended]
    CyclingTemp -->|Yes| CyclingWind{Wind < 30 km/h?}
    CyclingWind -->|No| CyclingBad
    CyclingWind -->|Yes| CyclingRain{Rain = 0mm/h?}
    CyclingRain -->|No| CyclingBad
    CyclingRain -->|Yes| CyclingGood[✅ Cycling Recommended]
    
    CyclingGood --> CheckRunning
    CyclingBad --> CheckRunning
    
    CheckRunning{Running Selected?}
    CheckRunning -->|Yes| EvalRunning[Evaluate Running Conditions]
    CheckRunning -->|No| ShowResults
    
    EvalRunning --> RunningTemp{Temperature in Range?}
    RunningTemp -->|No| RunningBad[❌ Running Not Recommended]
    RunningTemp -->|Yes| RunningWind{Wind < 30 km/h?}
    RunningWind -->|No| RunningBad
    RunningWind -->|Yes| RunningRain{Rain < 3mm/h?}
    RunningRain -->|No| RunningBad
    RunningRain -->|Yes| RunningGood[✅ Running Recommended]
    
    RunningGood --> ShowResults[Display Results]
    RunningBad --> ShowResults
    
    ShowResults --> AnyGood{Any Sport Recommended?}
    AnyGood -->|Yes| ShowSports[Show Sport Cards with Reasoning]
    AnyGood -->|No| ShowNone[Show: No Outdoor Sports Recommended]
    
    ShowSports --> End[Render UI]
    ShowNone --> End
    
    style Start fill:#e1ffe1
    style CyclingGood fill:#90EE90
    style RunningGood fill:#90EE90
    style CyclingBad fill:#FFB6C1
    style RunningBad fill:#FFB6C1
    style ShowNone fill:#FFB6C1
    style End fill:#e1f5ff
```

## User Preference Management

```mermaid
stateDiagram-v2
    [*] --> CheckStorage: Page Load
    
    CheckStorage --> LoadDefaults: No Preferences Found
    CheckStorage --> LoadSaved: Preferences Exist
    
    LoadDefaults --> DisplayUI: Apply Default Values
    LoadSaved --> DisplayUI: Apply Saved Values
    
    DisplayUI --> Idle: Show Current Preferences
    
    Idle --> EditMode: User Clicks Edit
    EditMode --> Validating: User Changes Value
    
    Validating --> Invalid: Validation Fails
    Validating --> Valid: Validation Passes
    
    Invalid --> EditMode: Show Error
    Valid --> SaveToStorage: Update Preference
    
    SaveToStorage --> RecalculateRecs: Store in Local Storage
    RecalculateRecs --> DisplayUI: Update Recommendations
    
    DisplayUI --> [*]: User Leaves
```

## Technology Stack Diagram

```mermaid
graph TB
    subgraph "Client Side"
        HTML[HTML5]
        CSS[Pure CSS]
        JS[JavaScript ES6+]
        Charts[Chart.js]
        LS[Local Storage API]
    end
    
    subgraph "Server Side"
        Python[Python 3.x]
        Django[Django Framework]
        Requests[Requests Library]
    end
    
    subgraph "External APIs"
        OWM[OpenWeatherMap API]
    end
    
    HTML --> CSS
    HTML --> JS
    JS --> Charts
    JS --> LS
    
    Django --> Python
    Django --> Requests
    Requests --> OWM
    
    Django -.->|Serves| HTML
    
    style HTML fill:#e1f5ff
    style Django fill:#ffe1e1
    style OWM fill:#e1ffe1
```

## Deployment Architecture

```mermaid
graph LR
    subgraph "Development Environment"
        Dev[Developer Machine]
        
        subgraph "Local Server"
            DjangoServer[Django Dev Server<br/>localhost:8000]
        end
        
        Browser[Web Browser]
    end
    
    subgraph "External Services"
        OWM[OpenWeatherMap<br/>api.openweathermap.org]
    end
    
    Dev -->|Runs| DjangoServer
    Browser -->|HTTP| DjangoServer
    DjangoServer -->|HTTPS| OWM
    
    style Dev fill:#fff4e1
    style DjangoServer fill:#ffe1e1
    style Browser fill:#e1f5ff
    style OWM fill:#e1ffe1
```

## File Structure

```
trivium-ai/
├── manage.py                      # Django management script
├── PRD.md                         # Product Requirements Document
├── ARCHITECTURE.md                # This file
│
├── weather_project/               # Django project directory
│   ├── __init__.py
│   ├── settings.py                # Django settings
│   ├── urls.py                    # URL routing
│   └── wsgi.py                    # WSGI configuration
│
├── weather_app/                   # Django application
│   ├── __init__.py
│   ├── views.py                   # View logic
│   ├── services/
│   │   ├── __init__.py
│   │   ├── weather_service.py     # OpenWeatherMap API integration
│   │   └── sport_service.py       # Sport recommendation logic
│   ├── templates/
│   │   └── index.html             # Single page template
│   └── static/
│       ├── css/
│       │   └── styles.css         # Pure CSS styling
│       └── js/
│           ├── charts.js          # Chart.js visualizations
│           ├── preferences.js     # Preference management
│           └── main.js            # Main application logic
│
└── requirements.txt               # Python dependencies
```

## API Integration Architecture

```mermaid
sequenceDiagram
    participant Django
    participant WeatherService
    participant Cache
    participant OWM as OpenWeatherMap
    
    Django->>WeatherService: get_weather_data(location)
    WeatherService->>Cache: Check Cache
    
    alt Cache Hit (< 10 min old)
        Cache-->>WeatherService: Return Cached Data
        WeatherService-->>Django: Weather Data
    else Cache Miss or Expired
        WeatherService->>OWM: GET /data/2.5/weather
        OWM-->>WeatherService: Current Weather
        WeatherService->>OWM: GET /data/2.5/forecast
        OWM-->>WeatherService: 24h Forecast
        WeatherService->>Cache: Store Data
        WeatherService-->>Django: Weather Data
    end
    
    Django->>Django: Process & Render
```

## Security Considerations

```mermaid
mindmap
  root((Security))
    API Keys
      Environment Variables
      Never Commit to Git
      Use .env File
    CORS
      Localhost Only in Dev
    Input Validation
      Preference Ranges
      Type Checking
    Data Privacy
      No Personal Data Stored
      Local Storage Only
      Anonymous Access
    API Rate Limiting
      Respect Free Tier Limits
      Cache Responses
      Handle Rate Limit Errors
```

## Performance Optimization Strategy

```mermaid
graph TD
    A[Performance Strategy] --> B[API Caching]
    A --> C[Minimal Dependencies]
    A --> D[Pure CSS Performance]
    A --> E[Local Storage]
    
    B --> B1[Cache Weather Data 10 min]
    B --> B2[Avoid Redundant API Calls]
    
    C --> C1[No CSS Frameworks]
    C --> C2[Lightweight Chart.js Only]
    
    D --> D1[No External CSS Files]
    D --> D2[Optimized Selectors]
    
    E --> E1[Instant Preference Load]
    E --> E2[No Server Round-trips]
    
    style A fill:#fff4e1
    style B fill:#e1ffe1
    style C fill:#e1f5ff
    style D fill:#ffe1e1
    style E fill:#e1f5ff
```

## Error Handling Flow

```mermaid
flowchart TD
    Start[User Action] --> TryAPI{API Call Needed?}
    
    TryAPI -->|Yes| APICall[Call OpenWeatherMap]
    TryAPI -->|No| LocalOp[Local Operation]
    
    APICall --> APISuccess{Success?}
    APISuccess -->|Yes| Process[Process Data]
    APISuccess -->|No| CheckError{Error Type?}
    
    CheckError -->|Network| ShowNetworkError[Show: Check Internet Connection]
    CheckError -->|Rate Limit| ShowRateError[Show: Too Many Requests, Try Later]
    CheckError -->|API Key| ShowKeyError[Show: Configuration Error]
    CheckError -->|Other| ShowGenericError[Show: Unable to Fetch Weather]
    
    LocalOp --> LocalSuccess{Success?}
    LocalSuccess -->|Yes| Process
    LocalSuccess -->|No| ShowLocalError[Show: Validation Error]
    
    Process --> UpdateUI[Update User Interface]
    ShowNetworkError --> LogError[Log Error]
    ShowRateError --> LogError
    ShowKeyError --> LogError
    ShowGenericError --> LogError
    ShowLocalError --> LogError
    
    LogError --> UpdateUI
    UpdateUI --> End[Complete]
    
    style Start fill:#e1ffe1
    style Process fill:#90EE90
    style ShowNetworkError fill:#FFB6C1
    style ShowRateError fill:#FFB6C1
    style ShowKeyError fill:#FFB6C1
    style ShowGenericError fill:#FFB6C1
    style ShowLocalError fill:#FFB6C1
    style End fill:#e1f5ff
```
