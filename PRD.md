# Product Requirements Document (PRD)
## Swiss Weather Sport Planner

### Project Overview
A Django web application that provides weather-based outdoor sport recommendations for Reinach BL, Switzerland. This is a personal learning project focused on helping users decide whether to go cycling or running based on current and forecasted weather conditions.

### Target Users
- Adults planning outdoor sports activities
- Non-tech-savvy users
- Focus on cycling and running enthusiasts in Reinach BL

### Core Features

#### 1. Weather Data Integration
- **Data Source**: OpenWeatherMap API
- **Location**: Reinach BL, Switzerland
- **Update Frequency**: Real-time (updates whenever source changes)
- **Data Types**: Temperature, precipitation, wind speed, rain radar
- **Forecast Range**: 24-hour forecast with daily summaries

#### 2. Sport Recommendations
- **Supported Sports**: Cycling and Running
- **Recommendation Logic**:
  - Temperature-based (user configurable with defaults)
  - Wind speed threshold: > 30 km/h discourages both sports
  - Rain threshold: 3mm/h cutoff (light rain OK for running, not for cycling)
  - Priority: Cycling preferred when both sports have good conditions
- **Display**: Show both sports side by side when conditions are good for both
- **Bad Weather Message**: "No outdoor sports recommended" when conditions are poor for all selected sports
- **Reasoning Display**: Show why each sport is/isn't recommended (e.g., "Cycling: Good - Temperature 20°C, Wind 15km/h")

#### 3. User Customization
- **Preferences Stored**: Local storage (browser)
- **Customizable Parameters**:
  - Sport selection (multiple sports can be selected)
  - Temperature ranges (min/max for each sport)
  - Wind tolerance
  - Rain threshold
- **Default Values**:
  - Cycling: 15-25°C optimal temperature
  - Running: 10-20°C optimal temperature
  - Wind: > 30 km/h not recommended
  - Rain: < 3mm/h for running, no rain for cycling
- **Editing**: Preferences editable directly on main page at any time

#### 4. User Interface
- **Type**: Single-page web application
- **Responsive**: Mobile browser and desktop compatible
- **Styling**: Pure CSS (no frameworks)
- **Layout Order**:
  1. Current weather conditions (displayed separately)
  2. Sport recommendations (side by side when multiple)
  3. Three charts displayed simultaneously:
     - Temperature forecast (24 hours)
     - Rain radar/precipitation (24 hours)
     - Wind speed (24 hours)
  4. User preference controls (on main page)

#### 5. Data Visualization
- **Charts**: Interactive charts/graphs
- **Timeframe**: 24-hour forecasts
- **Chart Types**:
  - Temperature line chart
  - Precipitation/rain bar chart or area chart
  - Wind speed line chart
- **Display**: All three charts visible at once (no tabs)

### Technical Architecture

#### Backend
- **Framework**: Django
- **Python Version**: To be confirmed by user
- **Server Type**: Development server (local hosting)
- **API Structure**: REST API if needed for frontend communication
- **Data Storage**: No database for historical data; real-time API calls only
- **Authentication**: None (anonymous access)

#### Frontend
- **Technology**: HTML, JavaScript, Pure CSS
- **Served By**: Django templates
- **State Management**: Local storage for user preferences
- **Charting Library**: To be determined (JavaScript library needed)

#### External APIs
- **Weather API**: OpenWeatherMap (free tier)
- **API Key**: User needs to register
- **Location**: Reinach BL coordinates

### User Flow
1. User visits single-page application
2. App displays current weather for Reinach BL
3. App shows sport recommendations based on default or saved preferences
4. User can view 24-hour forecast charts for temperature, rain, and wind
5. User can edit preferences directly on the page
6. Preferences are saved to local storage
7. Sport recommendations update based on new preferences

### Non-Functional Requirements
- **Performance**: Real-time weather updates
- **Usability**: Simple interface for non-tech-savvy users
- **Accessibility**: Mobile-responsive design
- **Scalability**: Personal project, not designed for scale
- **Cost**: Free service using free API tier

### Out of Scope
- User accounts/authentication
- Historical weather data storage
- Multiple locations beyond Reinach BL
- Sports beyond cycling and running
- Weather alerts or notifications
- Social sharing features
- Progressive Web App (PWA) features

### Success Criteria
- Successfully fetches and displays weather data from OpenWeatherMap
- Accurately recommends sports based on weather conditions
- User preferences persist across browser sessions
- Responsive design works on mobile and desktop
- Charts clearly visualize 24-hour weather forecasts
- Project completed within one day (learning timeline)

### Timeline
- **Target Completion**: Today (one-day project)
- **Phases**:
  1. Django project setup
  2. OpenWeatherMap API integration
  3. Frontend development with pure CSS
  4. User preference management with local storage
  5. Chart implementation
  6. Testing and refinement

### Compliance & Legal
- **Weather Data**: No licensing restrictions confirmed
- **API Terms**: Must comply with OpenWeatherMap free tier terms of service
- **Privacy**: No user data collected (anonymous access, local storage only)
