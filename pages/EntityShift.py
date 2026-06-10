{
  "name": "Shift",
  "type": "object",
  "properties": {
    "name": {
      "type": "string",
      "description": "Shift name (e.g., Morning, Night)"
    },
    "start_time": {
      "type": "string",
      "description": "Shift start time (HH:MM format)"
    },
    "end_time": {
      "type": "string",
      "description": "Shift end time (HH:MM format)"
    },
    "expected_hours": {
      "type": "number",
      "default": 8
    },
    "days_of_week": {
      "type": "array",
      "items": {
        "type": "string",
        "enum": [
          "monday",
          "tuesday",
          "wednesday",
          "thursday",
          "friday",
          "saturday",
          "sunday"
        ]
      }
    },
    "assigned_employees": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "employee_id": {
            "type": "string"
          },
          "employee_name": {
            "type": "string"
          }
        }
      }
    },
    "location": {
      "type": "string"
    },
    "department": {
      "type": "string"
    },
    "is_active": {
      "type": "boolean",
      "default": true
    },
    "color": {
      "type": "string",
      "description": "Color code for calendar display"
    }
  },
  "required": [
    "name",
    "start_time",
    "end_time"
  ]
}
