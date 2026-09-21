const deploy_connection = "api.tracky.boldbyte.dev/";
const dev_connection = "http://localhost:8010/";

async function user_signin(username, password) {
  try {
    const response = await fetch(`${dev_connection}login`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        username: username,
        password: password,
      }),
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json();

    return data;
  } catch (error) {
    console.error("Error signing in", error);
    throw error;
  }
}

async function create_user(username = "", password = "") {
  try {
    const response = await fetch(`${dev_connection}createUser`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        username: username,
        password: password,
      }),
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.text();
    console.log(data, response.status);

    return data;
  } catch (error) {
    console.error("Error creating user:", error);
    throw error;
  }
}

// Items
async function create_item(itemName = "", itemDesc= "", itemPrice = 0.0) {
  try {
    const response = await fetch(`${dev_connection}createItem`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        token: window.sessionStorage.getItem("sessionToken"),
        itemName: itemName,
        itemDesc: itemDesc,
        itemPrice: itemPrice,
      }),
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.text();
    console.log(data, response.status);

    return data;
  } catch (error) {
    console.error("Error creating item:", error);
    throw error;
  }
}
