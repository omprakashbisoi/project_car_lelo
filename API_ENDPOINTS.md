# Car Lelo - Complete API Documentation

**Base URL:** `http://localhost:8000/api/`

---

## 📋 Table of Contents
1. [Account API](#account-api)
2. [Seller API](#seller-api)
3. [Buyer API](#buyer-api)
4. [Wishlist API](#wishlist-api)
5. [Notification API](#notification-api)

---

## 🔐 Account API
**Base Path:** `/api/account/`

### 1. Register Email
- **Endpoint:** `POST /api/account/register/`
- **Permission:** AllowAny
- **Request Body:**
  ```json
  {
    "email": "user@example.com"
  }
  ```
- **Response:** OTP sent successfully
- **Status Code:** 200

### 2. Verify Email OTP
- **Endpoint:** `POST /api/account/register/verify-otp/`
- **Permission:** AllowAny
- **Request Body:**
  ```json
  {
    "otp": "123456",
    "email": "user@example.com" (optional, from session)
  }
  ```
- **Response:** Email verified successfully
- **Status Code:** 200

### 3. Complete Registration
- **Endpoint:** `POST /api/account/register/complete/`
- **Permission:** AllowAny
- **Request Body:**
  ```json
  {
    "username": "johndoe",
    "phone": "9876543210",
    "first_name": "John",
    "last_name": "Doe",
    "age": 25,
    "password": "securepass123",
    "confirm_password": "securepass123"
  }
  ```
- **Response:** User created successfully (with user details)
- **Status Code:** 201

### 4. Login
- **Endpoint:** `POST /api/account/login/`
- **Permission:** AllowAny
- **Request Body:**
  ```json
  {
    "username": "johndoe",
    "password": "securepass123"
  }
  ```
- **Response:** User logged in (with user details)
- **Status Code:** 200

### 5. Get Current User
- **Endpoint:** `GET /api/account/me/`
- **Permission:** IsAuthenticated
- **Response:** Current user details
- **Status Code:** 200

### 6. Logout
- **Endpoint:** `POST /api/account/logout/`
- **Permission:** IsAuthenticated
- **Response:** Logged out successfully
- **Status Code:** 200

### 7. Password Reset Request
- **Endpoint:** `POST /api/account/password/reset/`
- **Permission:** AllowAny
- **Request Body:**
  ```json
  {
    "email": "user@example.com"
  }
  ```
- **Response:** OTP sent to email
- **Status Code:** 200

### 8. Verify Password Reset OTP
- **Endpoint:** `POST /api/account/password/verify-otp/`
- **Permission:** AllowAny
- **Request Body:**
  ```json
  {
    "otp": "123456"
  }
  ```
- **Response:** OTP verified successfully
- **Status Code:** 200

### 9. Confirm Password Reset
- **Endpoint:** `POST /api/account/password/confirm/`
- **Permission:** AllowAny
- **Request Body:**
  ```json
  {
    "password": "newpass123",
    "confirm_password": "newpass123"
  }
  ```
- **Response:** Password changed successfully
- **Status Code:** 200

---

## 🚗 Seller API
**Base Path:** `/api/seller/`

### 1. Sell Car
- **Endpoint:** `POST /api/seller/sell-car/`
- **Permission:** IsAuthenticated
- **Request Body:**
  ```json
  {
    "brand": "Toyota",
    "car_model": "Fortuner",
    "variant": "4x4",
    "year": 2022,
    "fuel_type": "diesel",
    "kilometers": "50000-100000",
    "reg_state": "MH",
    "price": 1500000,
    "description": "Well maintained car"
  }
  ```
- **Response:** Car created successfully
- **Status Code:** 201

### 2. Add Car Location
- **Endpoint:** `POST /api/seller/sell-car/location/<car_id>/`
- **Permission:** IsAuthenticated
- **Request Body:**
  ```json
  {
    "city": "Pune",
    "state": "MH",
    "pin": "411001",
    "location_type": "car"
  }
  ```
- **Response:** Location added with coordinates
- **Status Code:** 201

### 3. Upload Car Image
- **Endpoint:** `POST /api/seller/sell-car/image-upload/<car_id>/`
- **Permission:** IsAuthenticated
- **Request:** Multipart Form Data
  ```
  - car_image: <image file>
  - img_type: "main" (or "side", "back", etc.)
  ```
- **Response:** Image uploaded successfully
- **Status Code:** 201

### 4. Get Dashboard Cars (List)
- **Endpoint:** `GET /api/seller/dashboard/cars/`
- **Permission:** IsAuthenticated
- **Response:** List of seller's cars
- **Status Code:** 200

### 5. Get Car Details (Detail)
- **Endpoint:** `GET /api/seller/dashboard/cars/<car_id>/`
- **Permission:** IsAuthenticated
- **Response:** Car details
- **Status Code:** 200

### 6. Update Car
- **Endpoint:** `PUT /api/seller/dashboard/cars/<car_id>/`
- **Permission:** IsAuthenticated
- **Request Body:** Car fields to update
- **Response:** Updated car details
- **Status Code:** 200

### 7. Partial Update Car
- **Endpoint:** `PATCH /api/seller/dashboard/cars/<car_id>/`
- **Permission:** IsAuthenticated
- **Request Body:** Partial car fields
- **Response:** Updated car details
- **Status Code:** 200

### 8. Delete Car
- **Endpoint:** `DELETE /api/seller/dashboard/cars/<car_id>/`
- **Permission:** IsAuthenticated
- **Response:** Car deleted successfully
- **Status Code:** 200

### 9. Toggle Car Availability
- **Endpoint:** `PATCH /api/seller/dashboard/cars/<car_id>/toggle-availability/`
- **Permission:** IsAuthenticated
- **Response:** `{"is_available": true/false}`
- **Status Code:** 200

### 10. Get Dashboard Images (List)
- **Endpoint:** `GET /api/seller/dashboard/images/`
- **Permission:** IsAuthenticated
- **Response:** List of seller's car images
- **Status Code:** 200

### 11. Get Image Details
- **Endpoint:** `GET /api/seller/dashboard/images/<image_id>/`
- **Permission:** IsAuthenticated
- **Response:** Image details
- **Status Code:** 200

### 12. Delete Image
- **Endpoint:** `DELETE /api/seller/dashboard/images/<image_id>/`
- **Permission:** IsAuthenticated
- **Response:** Image deleted successfully
- **Status Code:** 200

---

## 🛒 Buyer API
**Base Path:** `/api/buyer/`

### 1. Get All Cars
- **Endpoint:** `GET /api/buyer/cars/`
- **Permission:** AllowAny
- **Query Parameters:**
  ```
  - page: Page number
  - search: Search term
  - ordering: Order by field
  ```
- **Response:** List of all available cars
- **Status Code:** 200

---

## ❤️ Wishlist API
**Base Path:** `/api/wishlist/`

### 1. Toggle Wishlist
- **Endpoint:** `POST /api/wishlist/<car_id>/`
- **Permission:** IsAuthenticated
- **Response:**
  ```json
  {
    "wished": true/false,
    "detail": "Car is added/removed from your wishlist"
  }
  ```
- **Status Code:** 200

---

## 🔔 Notification API
**Base Path:** `/api/notification/`

### 1. Get All Notifications
- **Endpoint:** `GET /api/notification/`
- **Permission:** IsAuthenticated
- **Response:**
  ```json
  {
    "notifications": [...],
    "buy_request_car_ids": [1, 2, 3]
  }
  ```
- **Status Code:** 200

### 2. Create Notification (Request)
- **Endpoint:** `POST /api/notification/create/<car_id>/<request_type>/`
- **Permission:** IsAuthenticated
- **Request Types:** `contact_request` or `buy_request`
- **Request Body:**
  ```json
  {
    "message": "Interested in this car"
  }
  ```
- **Response:** Request created successfully
- **Status Code:** 201

### 3. Accept/Reject Request
- **Endpoint:** `POST /api/notification/action/<req_id>/<action>/`
- **Permission:** IsAuthenticated
- **Actions:** `accepted` or `rejected`
- **Response:** Request processed successfully
- **Status Code:** 200

### 4. Mark Notifications as Read
- **Endpoint:** `POST /api/notification/mark-as-read/`
- **Permission:** IsAuthenticated
- **Request Body:**
  ```json
  {
    "notification_ids": [1, 2, 3],
    "mark_all": false
  }
  ```
  OR
  ```json
  {
    "mark_all": true
  }
  ```
- **Response:** Notifications marked as read
- **Status Code:** 200

---

## 📝 Notification Types

| Type | Description |
|------|-------------|
| `contact_request` | Buyer requests seller's contact |
| `buy_request` | Buyer expresses interest in buying |
| `contact_shared` | Seller shared contact info |
| `buy_confirmation` | Sale confirmed |
| `sell_confirmation` | Seller confirmed sale |

---

## 🔐 Authentication

- **Session-based Authentication** (Django Sessions)
- **Token Support** (DRF Token Authentication)

### Headers for Authenticated Requests:
```
Authorization: Token <your-token>
```
OR use Django session cookies for browser requests.

---

## ✅ Common Response Codes

| Code | Meaning |
|------|---------|
| 200 | OK - Request successful |
| 201 | Created - Resource created |
| 400 | Bad Request - Invalid input |
| 401 | Unauthorized - Authentication required |
| 403 | Forbidden - No permission |
| 404 | Not Found - Resource doesn't exist |
| 429 | Too Many Requests - Rate limit exceeded |

---

## 📦 Example Complete Flow

### 1. User Registration Flow
```
POST /api/account/register/ → Get OTP
POST /api/account/register/verify-otp/ → Verify Email
POST /api/account/register/complete/ → Create Account
```

### 2. Seller Car Upload Flow
```
POST /api/seller/sell-car/ → Create Car
POST /api/seller/sell-car/location/<car_id>/ → Add Location
POST /api/seller/sell-car/image-upload/<car_id>/ → Add Images
```

### 3. Buyer Purchase Flow
```
GET /api/buyer/cars/ → Browse Cars
POST /api/wishlist/<car_id>/ → Add to Wishlist
POST /api/notification/create/<car_id>/buy_request/ → Send Buy Request
POST /api/notification/action/<req_id>/accepted/ → Wait for Approval
```

---

## 🚀 Status

✅ All API endpoints created and working
✅ Authentication implemented
✅ Permissions configured
✅ Database migrations applied

Last Updated: June 20, 2026
