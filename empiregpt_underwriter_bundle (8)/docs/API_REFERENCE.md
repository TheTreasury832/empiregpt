# EmpireGPT API Documentation

## 🔐 Authentication
All endpoints require an `x-api-key` header:
```
x-api-key: your_api_key_here
```

---

## 📩 POST /underwrite

Underwrite a single property.

### Request Body (JSON)
```json
{
  "address": "123 Main St, TX",
  "rehab_cost": 30000
}
```

### Example cURL
```bash
curl -X POST http://yourdomain/api/underwrite \
  -H "x-api-key: your_api_key_here" \
  -H "Content-Type: application/json" \
  -d '{"address": "123 Main St, TX", "rehab_cost": 30000}'
```

---

## 📩 POST /batch

Upload a CSV file of addresses for bulk underwriting.

### CSV Format
| address        |
|----------------|
| 123 Main St TX |
| 456 Oak Ave TX |

### Example cURL
```bash
curl -X POST http://yourdomain/api/batch \
  -H "x-api-key: your_api_key_here" \
  -F "file=@deals.csv"
```