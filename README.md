# WCO Hackathon 2026: The "Brain" of Customs
**Location:** Abu Dhabi, UAE  
**Theme:** Customs Agility in a Complex World

## 🚀 Mission Brief
Welcome, Developers!
You have been recruited to build the **Intelligence Engine** for the next generation of Customs Borders. 

With the explosion of E-Commerce, we can no longer check every package physically. We need **Algorithms** to detect fraud, calculate revenue, and protect society. Your goal is to operationalize the **WCO Framework of Standards on Cross-Border E-Commerce**.

## 📂 The Data
You are provided with a synthetic dataset representing **10,000 real-time E-Commerce Orders** entering Abu Dhabi.

* **File:** `data/auh_customs_2026_hackathon.zip` (Compressed CSV)
* **Context:** This data simulates a raw feed from a major online marketplace sent to Customs before the plane lands..

### Data Dictionary
| Column | Description |
| :--- | :--- |
| `order_id` | Unique identifier for the transaction |
| `timestamp` | Date and time the order was placed |
| `importer_name` | Name of the person importing the goods |
| `delivery_address` | Local address in Abu Dhabi |
| `product_title` | Short name of the item |
| `description` | Detailed commercial description (crucial for HS Codes) |
| `product_category` | Marketplace category tree |
| `item_price_inr` | Price in Indian Rupees (Source Currency) |
| `image_url` | Link to product image (Safe for Work filtered) |

---

## 🏆 The Challenge Levels

Your solution must process the CSV file and output results for the following 4 Logic Gates:

### 1️⃣ Level 1: The Identity Engine (Split Shipments)
* **Goal:** Detect people trying to evade customs limits by splitting orders.
* **Logic:** Identify **Same Importer + Same Day**.
* **Flag:** Any importer with multiple orders on the same calendar day where the *combined* value exceeds the limit.

### 2️⃣ Level 2: The Classification Engine (HS Codes)
* **Goal:** Assign a 6-digit HS Code to every item.
* **Logic:** Use NLP/ML on the `description` and `product_title`.
* **Output:** Predicted HS Code (e.g., `6203.42` for Men's Trousers).

### 3️⃣ Level 3: The Valuation Engine (Revenue)
* **Goal:** Calculate how much Duty is owed.
* **Rules:**
    1. **Convert Currency:** `AED = INR * 0.044`
    2. **De Minimis Threshold:** 1,000 AED.
    3. **Logic:** - Calculate the **Daily Total Value (AED)** for the importer.
       - If Daily Total <= 1,000 AED: **Duty = 0 (Exempt)**.
       - If Daily Total > 1,000 AED: **Duty applies to all items**.
    4. **Calculation:** `Duty = Item Value (AED) * 5%` (Assume standard 5% tariff for this challenge).

### 4️⃣ Level 4: The Protection Engine (Safety)
* **Goal:** Flag high-risk items regardless of value.
* **Reference:** See `documents/Risk_Profile_Alert.pdf` for specific targeting keywords (e.g., Drones, Weapons, Lithium Batteries).


**Good Luck! 🦅**
