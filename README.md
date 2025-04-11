# 🛒 Intellicart – Personalized Recommender System

Intellicart is a smart and simple product recommendation system designed for e-commerce platforms. It uses customer interaction data to suggest relevant products using a multi-agent AI structure.

## 📌 Project Overview

-  Recommends products based on customer browsing history
-  Built with Python, Streamlit, and SQLite
-  Uses customer, product, and recommendation agents
-  Simple user interface for selecting customers and viewing recommendations

## 🗂️ Project Files

| File/Folder                      | Description                                   |
|----------------------------------|-----------------------------------------------|
| `app.py`                        | Streamlit web app interface                   |
| `main.py`                       | Initializes database and loads CSV data       |
| `customer_data_collection.csv`  | Customer dataset                              |
| `product_recommendation_data.csv` | Product dataset                            |
| `ecommerce.db`                  | SQLite database (generated automatically)     |
| `requirements.txt`              | Required Python libraries                     |
| `README.md`                     | This file                                     |

---

## ⚙️ How to Run the Project

1. **Install dependencies**

```bash
pip install -r requirements.txt
```

2. **Initialize the database**

```bash
python main.py
```

3. **Run the Streamlit web app**

```bash
streamlit run app.py
```

4. **Open your browser and go to**

```
http://localhost:8501
```

## 👥 Team

- Pragya Agarwal
- Shashwat Tripathi

## 📜 License

This project is open-source and free to use for educational and non-commercial purposes.


## 🙌 Acknowledgements

Thanks to the mentors and organizers of **Hack the Future: A Gen AI Sprint** for this opportunity.
