
import os
import json
import urllib.request
import urllib.error

from mcp.server.mcpserver import MCPServer


# ==========================================
# 1. CREATE MCP SERVER
# ==========================================

mcp = MCPServer("MyFirstMCP")


# ==========================================
# 2. MCP TOOL - SEND CRM DATA TO N8N
# ==========================================

@mcp.tool()
def send_lead_to_n8n(
    Campaign: str = "",
    CustomerType: str = "",
    CustomerSubType: str = "",
    customerName: str = "",
    ContactNumber: str = "",
    Email: str = "",
    city: str = "",
    location: str = "",
    sublocation: str = "",
    GoogleMap: str = "",
    AgeOfProperty: str = "",
    Area: str = "",
    Price: str = "",
    Adderess: str = "",
    PropertyDetails: str = "",
    Facillities: str = "",
    TotalUnits: str = "",
    Dates: str = "",
    ReferenceId: str = "",
    Description: str = "",
    WebsiteURL: str = "",
    CreatedDate: str = "",
    UpdatedDate: str = ""
) -> str:

    """
    Send real estate CRM lead data to n8n
    using the configured Webhook URL.
    """

    # ======================================
    # 3. N8N WEBHOOK URL
    # ======================================

    webhook_url = os.environ.get(
        "N8N_WEBHOOK_URL",
        "https://automation.ibigdata.in/webhook/crm-data"
    )

    # ======================================
    # 4. PREPARE CRM DATA
    # ======================================

    payload = {
        "Campaign": Campaign,
        "CustomerType": CustomerType,
        "CustomerSubType": CustomerSubType,
        "customerName": customerName,
        "ContactNumber": ContactNumber,
        "Email": Email,
        "city": city,
        "location": location,
        "sublocation": sublocation,
        "GoogleMap": GoogleMap,
        "AgeOfProperty": AgeOfProperty,
        "Area": Area,
        "Price": Price,
        "Adderess": Adderess,
        "PropertyDetails": PropertyDetails,
        "Facillities": Facillities,
        "TotalUnits": TotalUnits,
        "Dates": Dates,
        "ReferenceId": ReferenceId,
        "Description": Description,
        "WebsiteURL": WebsiteURL,
        "CreatedDate": CreatedDate,
        "UpdatedDate": UpdatedDate
    }

    # ======================================
    # 5. CONVERT DATA INTO JSON
    # ======================================

    data = json.dumps(
        payload,
        ensure_ascii=False
    ).encode("utf-8")

    # ======================================
    # 6. PREPARE HTTP REQUEST
    # ======================================

    headers = {
        "Content-Type": "application/json"
    }

    # Optional webhook authentication
    webhook_secret = os.environ.get(
        "N8N_WEBHOOK_SECRET"
    )

    if webhook_secret:
        headers["X-Webhook-Secret"] = webhook_secret

    request = urllib.request.Request(
        url=webhook_url,
        data=data,
        headers=headers,
        method="POST"
    )

    # ======================================
    # 7. SEND DATA TO N8N
    # ======================================

    try:
        with urllib.request.urlopen(
            request,
            timeout=30
        ) as response:

            response_body = response.read().decode(
                "utf-8",
                errors="replace"
            )

            return (
                "CRM data sent to n8n.\n"
                f"HTTP Status: {response.status}\n"
                f"n8n Response: {response_body}"
            )

    # ======================================
    # 8. HANDLE HTTP ERRORS
    # ======================================

    except urllib.error.HTTPError as error:

        error_body = error.read().decode(
            "utf-8",
            errors="replace"
        )

        return (
            f"HTTP Error {error.code}: "
            f"{error_body}"
        )

    except urllib.error.URLError as error:

        return (
            f"Connection failed: {error.reason}"
        )

    except Exception as error:

        return (
            f"Request failed: "
            f"{type(error).__name__}: {error}"
        )


# ==========================================
# 9. START MCP SERVER
# ==========================================

if __name__ == "__main__":

    port = int(
        os.environ.get("PORT", "8000")
    )

    print("Starting Gemini CRM MCP Server...")
    print(f"Port: {port}")
    print("n8n CRM Webhook configured.")

    mcp.run(
        transport="streamable-http",
        host="0.0.0.0",
        port=port
    )
