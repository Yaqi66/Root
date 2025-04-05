# 🌱 ROOT — Smart Plant Care Powered by Raspberry Pi & Azure

**ROOT** is an intelligent, Raspberry Pi-powered system that cares for your plants so you don't have to.

Whether you're traveling or just stuck at work, ROOT keeps an eye on your leafy friends with a camera module, sensors, and powerful AI—ensuring they get the attention they deserve, anytime, anywhere.

---

## 🚀 Features

### 📸 Hourly Monitoring
A camera module captures plant images every hour, which are sent to a **custom-trained Azure Computer Vision model** to:
- Identify the plant species
- Detect early signs of disease

### 🌡️ Environmental Sensing
Onboard sensors track:
- Temperature  
- Humidity  
- Soil moisture *(planned feature)*

All sensor data is stored in an **Azure SQL Database** for real-time monitoring and future insights.

### 🤖 AI-Powered Care Suggestions
Environmental and visual data are sent to **Azure OpenAI**, which generates **custom care recommendations** tailored to your specific plant and its environment.

### 🛰️ Remote Access
View plant images and status from anywhere via a secure dashboard — perfect for plant lovers on the go.

---

## 🛠️ Future Development

- 💧 **Automated Irrigation**  
  A **relay-controlled water pump** is in development and will activate automatically when low soil moisture is detected.

- 🌾 **Scalability**  
  The system is designed with future support for **mechanized, large-scale farming**, enabling fully automated agriculture.

---

## 📦 Tech Stack

- **Hardware**: Raspberry Pi 5, Pi Camera, DHT22 (temperature & humidity sensor), planned soil moisture sensor, relay
- **Cloud Services**:
  - Azure Custom Vision
  - Azure SQL Database
  - Azure OpenAI
- **Languages**: Python, SQL
- **APIs**: RESTful integration with Azure endpoints

---
