# Global Weather Data ：开源免费的全球气象数据库 / Open-Source & Free Global Weather Database


<div align="center">

🌐 **[English Version](#-global-weather-data--open-source--free-global-weather-database)** | 🇨🇳 **[中文简体版本](#-global-weather-data--开源免费的全球气象数据库)**

</div>

---

<div id="-global-weather-data--open-source--free-global-weather-database"></div>

# Global Weather Data: Open-Source & Free Global Weather Database

🌐 **Official Website:** [global-weather-data.com](https://global-weather-data.com/) 

![Homepage English](figures/home_en.png)

Global Weather Data is a professional platform dedicated to providing free global weather forecast data and historical meteorological data for downloading, querying, and visual display. It aims to offer the easiest and most accessible data acquisition channels for global developers, researchers, and weather enthusiasts entirely free of charge. Users can directly view and download CSV data via the web interface or retrieve real-time weather and historical data programmatically through clean and efficient RESTful APIs. All weather forecasts and historical datasets are provided completely free of charge.

## 🚀 Key Features

- **City Weather Forecasts:** 15-day hourly forecasts for over 12,000 global settlements (covering towns, cities, and local regions) with 20+ meteorological variables.
- **Global Grid Forecasts:** 15-day hourly forecast data on a global 0.25° grid, ideal for spatial heatmaps, geographic boundary overlays, and machine learning model training inputs.
- **Historical Weather Archive:** Over 10 years of hourly historical records for 12,000+ global locations sourced from ERA5, covering 20+ meteorological variables.
- **Dual-Mode Data Access:** Support for one-click CSV data export via the web interface or automated retrieval through API endpoints.

---

## 📊 Core Data Modules

### 1. City Weather Forecast Data
- **Search & Localization:** The top search bar supports intelligent queries using global place names in any language, latitude/longitude coordinates, or GeoNames IDs (`geonameID`), automatically matching the most precise location.
- **Data Source:** Powered by authoritative ECMWF forecast models.
- **Meteorological Variables:** 20+ hourly high-resolution meteorological elements including temperature, pressure, wind speed, wind direction, relative humidity, solar radiation, soil temperature, soil moisture, and runoff.
- **Access Methods:**
  * **Web Visualization:** Real-time loading of 15-day trend charts with a one-click button to download full CSV datasets.
  * **API Online Retrieval:** A real-time API testing tool at the bottom of the page that dynamically builds request URLs using location names, IDs, or coordinates.

![Forecast English](figures/forecast_en.png)

### 2. Grid Forecast Data (0.25° Grid)
- **Spatial Grid Queries:** Specify latitude/longitude bounds, meteorological variables, and time parameters to retrieve structured grid forecasts for any region worldwide.
- **Use Cases:** Directly overlay geographic boundaries to render heatmaps or contour maps, or seamlessly import data into meteorological and environmental machine learning models for training.

![Grid English](figures/grid_en.png)

### 3. Historical Weather Data
- **Long-Term Temporal Span:** Provides precise historical weather records spanning over 10 years with hourly resolution.
- **Data Source:** Powered by ERA5 reanalysis datasets (Note: Due to reanalysis publication cycles, the latest historical data typically has a lag of approximately 7 to 10 days).
- **Flexible Retrieval:** Adjust location and past-day parameters in the API to freely acquire continuous hourly weather archives for past days, months, or years.

![History English](figures/history_en.png)

---

## 🔌 API Quick Start

The platform APIs are lightweight and ready out-of-the-box. Simply specify the target location (place name, ID, or coordinates) for instant responses.

### Global Weather Forecast API Request Structure
```http
GET https://global-weather-data.com/api/forecast/Shanghai/ueUR6IpBRsz6AL8W6Nm1VIAOv
```
Requires 2 parameters:
- `location` (or coordinates/ID), e.g., `Shanghai`.
- `api_key`, e.g., `ueUR6IpBRsz6AL8W6Nm1VIAOv` (available in your personal center).

The location parameter accepts place names in any language, latitude/longitude coordinates (longitude first, latitude second, comma-separated), or GeoNames IDs (`geonameID`) covering 12,000+ settlements with populations over 50,000. Returns 15-day hourly weather forecasts including temperature, pressure, humidity, cloud cover, radiation, and precipitation (20+ variables).

### Global Regional Grid Weather Forecast API Request Structure
```http
GET https://global-weather-data.com/api/grid_forecast/111/113/31/43/202611111715/t2m/ueUR6IpBRsz6AL8W6Nm1VIAOv
```
Requires 7 URL path parameters:
- Bounding box coordinates: `111`, `113`, `31`, `43` representing longitudes 111°–113° and latitudes 31°–43°.
- Time: `202611111715` (November 11, 2026, 17:15, hourly precision recommended).
- Meteorological variable: `t2m` (2-meter temperature / `temperature_2m`, supporting 20+ variables).
- `api_key`: Available in your personal center.

Returns a 2D array of 0.25° gridded weather forecast data for the specified region and time.

### Global Historical Weather Data API Request Structure
```http
GET https://global-weather-data.com/api/history/Paris/30/243jj23JD7wj3WIEU943jjeWOI43
```
Requires 3 parameters:
- `location` (or coordinates/ID), e.g., `Paris`.
- `recent_days`, e.g., `30` (representing hourly historical weather data for the past 30 days).
- `api_key`, e.g., `243jj23JD7wj3WIEU943jjeWOI43` (available in your personal center).

Returns hourly historical weather records for the past 30 days for the specified location, covering 20+ variables. Due to reanalysis updating lags, the latest data is typically available up to ~10 days prior to the current date.

For complete API parameter descriptions, response formats, and detailed physical definitions and unit reference tables for all meteorological variables, please visit the [Global Weather Data Official Website](https://global-weather-data.com/).

### Data Visualization Examples:

![Shortwave Radiation Eastern China](figures/str_2026-09-13_070000_provinces.png)
> UTC 2026-09-12 18:00 Shortwave Radiation Forecast in Eastern China (Next 13 Hours)

![Los Angeles 15-Day Forecast](figures/Los_Angeles_15_day_forecast.png)
> November 3–18, 2026 Los Angeles 15-Day Hourly Weather Forecast (23 Meteorological Variables)

![Global Shortwave Radiation Forecast](figures/ssrd_2026-09-14_124000_provinces.png)
> UTC 2026-09-13 18:00 Global Shortwave Radiation Forecast (Next 13 Hours)

![Global 2m Temperature Forecast](figures/t2m_2026-09-14_080000_provinces.png)
> UTC 2026-09-14 08:00 Global 2-Meter Temperature Forecast (Next 38 Hours)

![Beijing Historical Chart](figures/beijing_history.png)
> Beijing Recent 30-Day Historical Meteorological Data Chart

---

## 📄 License & Statements

All meteorological data and services provided on the platform are subject to relevant terms of use and open-source licenses; please refer to the official website for details. The project source code is open-sourced under the MIT License. This project is entirely free and open to global users without any charges for data query and download features. Daily storage, processing, and update costs are personally borne by the developer. Users can optionally support the project by upgrading to an annual professional user subscription.

Weather data provided by ECMWF under CC-BY 4.0 license.

---

<div id="-global-weather-data--开源免费的全球气象数据库"></div>

# Global Weather Data ：开源免费的全球气象数据库

<div align="center">

🌐 **[English Version](#-global-weather-data--open-source--free-global-weather-database)** | 🇨🇳 **[中文简体版本](#-global-weather-data--开源免费的全球气象数据库)**

</div>

---

🌐 **官方网站：** [global-weather-data.com](https://global-weather-data.com/) 

![主页中文](figures/home_cn.png)

Global Weather Data 是一个专注于全球天气预报数据与历史气象数据下载、查询及可视化展示的专业平台。旨在免费为全球开发者、研究人员及气象爱好者提供最便捷的数据获取途径，用户既可以通过网页端直接查看与下载 CSV 数据，也可以通过简洁高效的 RESTful API 在线调取全网气象数据。所有天气预报数据和历史天气数据均免费提供。

## 🚀 核心功能概述

- **城市天气预报：** 提供全球 12,000+ 个居民地（覆盖城镇与乡村）未来 15 天、逐小时、20+ 种气象变量的预报数据。
- **网格天气预报：** 提供全球 0.25° 分辨率的网格预报数据，覆盖未来 15 天逐小时空间网格，支持热力图绘制与模型训练输入。
- **历史天气数据：** 提供全球 12,000+ 城镇过去 10 年以上、逐小时、20+ 气象变量的长序列历史气象档案。
- **双模数据获取：** 支持网页端一键导出 CSV 格式数据，或通过 API 接口进行程序化自动调用。

---

## 📊 核心数据模块介绍

### 1. 城市天气预报数据
- **搜索与定位：** 顶部搜索栏支持全球任意语言地名、经纬度坐标或 GeoNames ID (`geonameID`) 进行智能检索，系统将自动匹配最精准的地点。
- **数据来源：** 依托 ECMWF 权威预报模型。
- **气象变量：** 提供气温、气压、风速、风向、相对湿度、太阳辐射、地温、土壤含水量、径流等 20 余种逐小时高分辨率气象要素。
- **获取方式：**
  * **网页可视化：** 实时加载未来 15 天趋势图表，点击右上角即可一键下载全量 CSV 数据。
  * **API 在线调取：** 页面下方提供实时 API 测试工具，支持通过地名、ID 或经纬度快速构建请求 URL。

![主页中文](figures/forecast_cn.png)

### 2. 网格预报数据 (0.25° 网格)
- **空间网格查询：** 通过指定经纬度范围、气象变量与时间参数，获取全球任意区域的结构化网格预报。
- **应用场景：** 可直接加载地理边界绘制热力图、色斑图，或无缝导入气象与环境机器学习模型中进行训练。

![主页中文](figures/grid_cn.png)

### 3. 历史天气数据
- **长序列时空跨度：** 提供跨度长达 10 年以上、逐小时分辨率的精确历史气象记录。
- **数据来源：** 依托 ERA5 再分析资料（注：受限于数据发布周期，最新历史数据通常存在 7–10 天左右的入库延迟）。
- **灵活调用：** 通过调整API中的地点与天数参数，可自由获取过去几天、几十天乃至数年的连续逐小时气象档案。

![主页中文](figures/history_cn.png)

---

## 🔌 API 快速上手

平台 API 设计轻量、开箱即用。只需指定目标地点（地名、ID 或经纬度）即可快速响应。

### 全球天气预报数据示例请求结构
```http
GET https://global-weather-data.com/api/forecast/Shanghai/ueUR6IpBRsz6AL8W6Nm1VIAOv
```
须传入以下2个参数：
- 地点（或经纬度、ID），如 `Shanghai`
- `api_key`，如 `ueUR6IpBRsz6AL8W6Nm1VIAOv`（可以在个人中心查看）

地点参数可以是地名、经纬度坐标或 GeoNames ID (geonameID)，支持全球12000+ 个5万人口以上居民地，任意语言地名均可，使用经纬度时经度在前纬度在后，逗号分隔。

返回该地点未来15日逐小时气象预报数据，包含气温、气压、湿度、云量、辐射、降水等20+种气象变量。

### 全球任意区域网格天气预报数据示例请求结构
```http
GET https://global-weather-data.com/api/grid_forecast/111/113/31/43/202611111715/t2m/ueUR6IpBRsz6AL8W6Nm1VIAOv
```
须传入以下7个参数：
- 经纬度范围：`111`、`113`、`31`、`43` 表示经度 111~113°，纬度 31~43° 方形区域
- 时间：`202611111715`（2026年11月11日17时15分，精确到小时即可）
- 气象变量：`t2m`（地面2米气温 / `temperature_2m`，支持20+气象变量）
- `api_key`：可以在个人中心查看

返回该时刻该经纬度范围区域 0.25° 网格气象预报数据（地面2米气温），为二维数组。

### 全球历史天气数据数据示例请求结构
```http
GET https://global-weather-data.com/api/history/Paris/30/243jj23JD7wj3WIEU943jjeWOI43
```
须传入以下3个参数：
- 地点（或经纬度、ID），如 `Paris`
- 最近天数：`30`（代表最近30日的逐小时历史天气数据）
- `api_key`：如 `243jj23JD7wj3WIEU943jjeWOI43`（可以在个人中心查看）

返回该地点最近30日逐小时历史天气数据，包含气温、气压、湿度、云量、辐射、降水等20+种气象变量。由于再分析数据的迟滞更新，最新数据在当前日期的前10天左右。

有关完整的 API 参数说明、请求响应格式以及所有气象变量的详细物理定义与单位对照表，请访问 [Global Weather Data 官网](https://global-weather-data.com/) 查看详细文档。

以下是一些数据可视化示例：

![主页中文](figures/str_2026-09-13_070000_provinces.png)
> UTC 2026-09-12 18:00 中国东部短波辐射预报（未来13小时）

![主页中文](figures/Los_Angeles_15_day_forecast.png)
> 2026年11月3日至18日 洛杉矶未来15日逐小时气象预报（23气象变量）

![主页中文](figures/ssrd_2026-09-14_124000_provinces.png)
> UTC 2026-09-13 18:00 全球短波辐射预报（未来13小时）

![主页中文](figures/t2m_2026-09-14_080000_provinces.png)
> UTC 2026-09-14 08:00 全球地面2米气温预报（未来38小时）

![主页中文](figures/beijing_history.png)
> 北京市最近30日历史气象数据图表

---

## 📄 许可与声明

平台所提供的所有气象数据与服务均遵循相关使用条款与开源协议，详情请参考官方网站说明。本项目代码按照 MIT 协议开源。本项目完全免费开放给全球使用，用户无需任何付费即可使用全部数据查询、下载功能，数据日常存储、处理、更新成本均由开发者个人担负，用户可以通过升级年付专业用户的方式对本项目进行捐助。

Weather data provided by ECMWF under CC-BY 4.0 license.