from broverse import state

# Set global configuration
state.set('model_name', 'claude-3-sonnet')
state.set('temperature', 0.7)
state.update(max_tokens=1000, debug=True)

# Access from anywhere in your code
print(f"Model: {state.get('model_name')}")
print(f"Temperature: {state.get('temperature')}")
print(f"Debug mode: {state.get('debug', False)}")

# Update values
state.set('temperature', 0.9)
print(f"Updated temperature: {state.get('temperature')}")

# List all state
print("All state:", dict(state.items()))