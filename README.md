# 🏗️ Solution Architecture

## 🌐 Overview

The solution integrates multiple technologies to deliver a robust dealership review platform. Users interact with the **Dealerships Website**, a Django-based web application, which communicates with various backend services to provide data and sentiment analysis.

---

## 🧩 Components & Services

### 1. 🚗 Dealerships Website (Django Application)

Users access the website via a web browser. The Django app exposes several microservices:

- `get_cars/` – Retrieve list of cars  
- `get_dealers/` – Retrieve list of dealers  
- `get_dealers/:state` – Retrieve dealers by state  
- `dealer/:id` – Retrieve dealer by ID  
- `review/dealer/:id` – Retrieve reviews for a specific dealer  
- `add_review/` – Submit a review for a dealer  

**Database:**  
Uses **SQLite** to store Car Make and Car Model data.

---

### 2. 🧾 Dealerships and Reviews Service (Express + MongoDB in Docker)

This service handles dealer and review data. It provides the following endpoints:

- `/fetchDealers` – Fetch all dealers  
- `/fetchDealer/:id` – Fetch dealer by ID  
- `/fetchReviews` – Fetch all reviews  
- `/fetchReview/dealer/:id` – Fetch reviews for a specific dealer  
- `/insertReview` – Insert a new review  

**Deployment:**  
Runs inside a **Docker container**.

---

### 3. 🔁 Django Proxy Service

The Django application includes a proxy layer that facilitates communication between the **Dealerships Website** and the **Dealerships and Reviews Service**.

---

### 4. 🧠 Sentiment Analyzer Service (IBM Cloud Code Engine)

This service analyzes the sentiment of review text. It offers the following endpoint:

- `/analyze/:text` – Returns sentiment classification: `positive`, `negative`, or `neutral`

**Integration:**  
The Django Proxy Service consumes this API to analyze user-submitted reviews.

---

## 🖼️ Architecture Diagram

![Solution Architecture](v2.capstone-dealership-architecture-1.png)
