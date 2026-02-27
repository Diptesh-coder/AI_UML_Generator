"""
Demo Script for AI UML Diagram Generator API
This demonstrates how to use the API programmatically
"""
import requests
import json


BASE_URL = "http://localhost:8000"


def test_basic_generation():
    """Test basic diagram generation"""
    print("=" * 60)
    print("Test 1: Basic Diagram Generation")
    print("=" * 60)
    
    # Sample SRS text
    text = """
    A Guest can register to become a Customer.
    The Customer adds Products to a Shopping Cart.
    Customer extends User.
    Admin extends User.
    Class Order has orderDate, totalAmount, status.
    Order contains OrderItems.
    Payment processes Orders.
    User has name, email, password.
    """
    
    response = requests.post(
        f"{BASE_URL}/api/generate",
        data={"text_input": text}
    )
    
    if response.status_code == 200:
        data = response.json()
        print("✅ Generation successful!")
        print(f"📊 Session ID: {data['session_id']}")
        print(f"📈 Overall Confidence: {data['diagram_data']['overall_confidence']:.2f}")
        print(f"📦 Classes found: {len(data['diagram_data']['classes'])}")
        print(f"🔗 Relationships found: {len(data['diagram_data']['relationships'])}")
        
        # Print classes
        print("\n📝 Classes:")
        for cls in data['diagram_data']['classes']:
            print(f"  • {cls['name']} (confidence: {cls['confidence']:.2f})")
        
        # Print relationships
        print("\n🔗 Relationships:")
        for rel in data['diagram_data']['relationships']:
            print(f"  • {rel['from_class']} --[{rel['relationship_type']}]--> {rel['to_class']}")
        
        return data['session_id']
    else:
        print(f"❌ Error: {response.status_code}")
        return None


def test_edit_operations(session_id):
    """Test editing operations"""
    print("\n" + "=" * 60)
    print("Test 2: Interactive Editing")
    print("=" * 60)
    
    if not session_id:
        print("⚠️  Skipping (no session ID)")
        return
    
    # Test 1: Add a new class
    print("\n➕ Adding new class 'Inventory'...")
    new_class = {
        "name": "Inventory",
        "attributes": [],
        "methods": [],
        "confidence": 0.9
    }
    
    response = requests.post(
        f"{BASE_URL}/api/edit/{session_id}/class",
        json=new_class
    )
    
    if response.status_code == 200:
        print("✅ Class added successfully!")
    else:
        print(f"❌ Failed to add class: {response.status_code}")
    
    # Test 2: Update a class
    print("\n✏️  Updating class 'User'...")
    updated_class = {
        "name": "User",
        "attributes": [
            {"name": "userId", "data_type": "UUID", "visibility": "-", "confidence": 0.95}
        ],
        "methods": [],
        "confidence": 0.95
    }
    
    response = requests.put(
        f"{BASE_URL}/api/edit/{session_id}/class/User",
        json=updated_class
    )
    
    if response.status_code == 200:
        print("✅ Class updated successfully!")
    else:
        print(f"❌ Failed to update class: {response.status_code}")
    
    # Test 3: Regenerate diagram
    print("\n🔄 Regenerating diagram...")
    response = requests.get(f"{BASE_URL}/api/regenerate/{session_id}")
    
    if response.status_code == 200:
        data = response.json()
        print("✅ Diagram regenerated!")
        print(f"📊 New diagram URL: {data['diagram_url']}")
    else:
        print(f"❌ Failed to regenerate: {response.status_code}")


def test_export_operations(session_id):
    """Test export operations"""
    print("\n" + "=" * 60)
    print("Test 3: Export Operations")
    print("=" * 60)
    
    if not session_id:
        print("⚠️  Skipping (no session ID)")
        return
    
    # Test JSON export
    print("\n📥 Exporting as JSON...")
    response = requests.get(f"{BASE_URL}/api/export/{session_id}/json")
    
    if response.status_code == 200:
        print("✅ JSON export successful!")
        print("📊 Sample data:")
        data = response.json()
        print(json.dumps(data, indent=2)[:500] + "...")
    else:
        print(f"❌ Failed to export JSON: {response.status_code}")
    
    # Test XMI export
    print("\n📥 Exporting as XMI...")
    response = requests.get(f"{BASE_URL}/api/export/{session_id}/xmi")
    
    if response.status_code == 200:
        print("✅ XMI export successful!")
        print("📊 Sample XMI:")
        print(response.text[:500] + "...")
    else:
        print(f"❌ Failed to export XMI: {response.status_code}")
    
    # Test PlantUML export
    print("\n📥 Exporting as PlantUML...")
    response = requests.get(f"{BASE_URL}/api/export/{session_id}/plantuml")
    
    if response.status_code == 200:
        print("✅ PlantUML export successful!")
        print("📊 PlantUML code:")
        print(response.text)
    else:
        print(f"❌ Failed to export PlantUML: {response.status_code}")


def test_advanced_srs():
    """Test with more complex SRS"""
    print("\n" + "=" * 60)
    print("Test 4: Advanced SRS (E-Commerce System)")
    print("=" * 60)
    
    text = """
    E-Commerce System Requirements:
    
    The system manages an online shopping platform with the following entities:
    
    User entity has userId, name, email, password, and registrationDate.
    Customer is a type of User.
    Admin is also a type of User with additional privileges.
    
    Product entity contains productId, name, description, price, stockQuantity.
    Category entity groups Products by name and description.
    Products belong to Categories.
    
    ShoppingCart is associated with Customer and contains Products.
    Each Customer has one ShoppingCart.
    ShoppingCart can contain multiple Products.
    
    Order entity has orderId, orderDate, status, and totalAmount.
    Customer places Orders.
    Order contains OrderItems.
    OrderItem links Products to Orders with quantity and price.
    
    Payment entity processes Orders.
    Payment has paymentId, amount, method, and paymentDate.
    Each Order can have one Payment.
    
    Review entity allows Customers to review Products.
    Review has rating, comment, and reviewDate.
    """
    
    response = requests.post(
        f"{BASE_URL}/api/generate",
        data={"text_input": text}
    )
    
    if response.status_code == 200:
        data = response.json()
        print("✅ Complex SRS processed successfully!")
        print(f"\n📊 Results:")
        print(f"   • Session ID: {data['session_id']}")
        print(f"   • Overall Confidence: {data['diagram_data']['overall_confidence']:.2%}")
        print(f"   • Classes: {len(data['diagram_data']['classes'])}")
        print(f"   • Relationships: {len(data['diagram_data']['relationships'])}")
        
        print(f"\n📦 Extracted Classes:")
        for cls in data['diagram_data']['classes']:
            attrs_count = len(cls['attributes'])
            methods_count = len(cls['methods'])
            print(f"   • {cls['name']:20s} (confidence: {cls['confidence']:.2f}, "
                  f"attrs: {attrs_count}, methods: {methods_count})")
        
        print(f"\n🔗 Extracted Relationships:")
        for rel in data['diagram_data']['relationships']:
            print(f"   • {rel['from_class']:15s} --[{rel['relationship_type']:12s}]--> "
                  f"{rel['to_class']:15s} (confidence: {rel['confidence']:.2f})")
        
        print(f"\n📊 PlantUML Preview:")
        print(data['plantuml_code'])
        
    else:
        print(f"❌ Error: {response.status_code}")


def main():
    """Run all tests"""
    print("🤖 AI UML Diagram Generator - API Demo")
    print("🔗 Testing server at:", BASE_URL)
    print()
    
    try:
        # Check if server is running
        response = requests.get(BASE_URL)
        if response.status_code != 200:
            print("❌ Server is not responding correctly")
            return
    except Exception as e:
        print(f"❌ Cannot connect to server: {e}")
        print("💡 Make sure the server is running: python app.py")
        return
    
    print("✅ Server is running!\n")
    
    # Run tests
    session_id = test_basic_generation()
    
    if session_id:
        test_edit_operations(session_id)
        test_export_operations(session_id)
    
    test_advanced_srs()
    
    print("\n" + "=" * 60)
    print("✅ All tests completed!")
    print("=" * 60)
    print("\n💡 Tips:")
    print("   • Open http://localhost:8000 in browser for interactive UI")
    print("   • Check outputs/ folder for generated diagrams")
    print("   • Review QUICKSTART.md for more examples")


if __name__ == "__main__":
    main()
