import React, { useState } from "react";
import axios from "axios";
import { useHistory } from "react-router-dom";

function LoginForm() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [group, setGroup] = useState("Tracked");
  const [isUser, setIsUser] = useState(true);
  const [error, setError] = useState("");
  const history = useHistory();

  const handleUsernameChange = (event) => {
    setUsername(event.target.value);
  };

  const handlePasswordChange = (event) => {
    setPassword(event.target.value);
  };

  const handleSubmit = (event) => {
    event.preventDefault();
    setError("");

    axios
      .post("http://127.0.0.1:8000/api/auth/login/", {
        username,
        password,
        group,
      })
      .then((response) => {
        if (!isUser) {
          history.push("/attendant", { params: response.data.name });
          history.go(0);
        } else {
          history.push("/user", {
            params: response.data.name,
            anotherParam: response.data.ucid,
          });
          history.go(0);
        }
      })
      .catch((error) => {
        setError("Invalid credentials. Please try again.");
      });
  };

  const handleLogout = (event) => {
    history.push("/");
    history.go(0);
  };

  return (
    <form onSubmit={handleSubmit}>
      <div style={styles.login}>
        <div style={styles.username}>
          <div>
            <label htmlFor="username">Enter UCID:</label>
            <input
              type="text"
              id="username"
              value={username}
              onChange={handleUsernameChange}
              style={styles.input}
            />
          </div>
          <div>
            <label htmlFor="password">Create Password:</label>
            <input
              type="password"
              id="password"
              value={password}
              onChange={handlePasswordChange}
              style={styles.input}
            />
          </div>
        </div>
        <div style={styles.errorMess}>{error}</div>
        <div>
          <button onClick={() => handleLogout()} style={styles.buttonStyles}>
            Back
          </button>
          <button type="submit" style={styles.buttonStyles}>
            Create
          </button>
        </div>
      </div>
    </form>
  );
}

const styles = {
  buttonStyles: {
    width: "60px",
    margin: "10px",
  },
  errorMess: {
    fontSize: "10px",
    color: "red",
  },
  appBackground: {
    color: "#db471a",
  },
  login: {
    position: "fixed",
    top: "50%",
    left: "50%",
    transform: "translate(-50%, -50%)",
    backgroundColor: "#F08000",
    fontSize: 18,
    fontWeight: "bold",
    lineHeight: 2.0,
    color: "#292b2c",
    borderRadius: 30,
    borderWidth: "thick",
    width: "35%",
    height: "250px",
  },
  username: {
    display: "flex",
    flexDirection: "column",
    alignItems: "center",
    justifyContent: "center",
    gap: "10px",
  },
  input: {
    boxSizing: "border-box",
    width: "100%",
    padding: "3px",
    borderRadius: "5px",
    border: "1px solid #ccc",
    outline: "none",
  },
};

export default LoginForm;
