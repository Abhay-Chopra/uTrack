import React, { useState } from "react";
import axios from "axios";

function LoginForm({ history }) {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [group, setGroup] = useState("");
  const [isUser, setIsUser] = useState(true);
  const [error, setError] = useState("");

  const handleUsernameChange = (event) => {
    setUsername(event.target.value);
  };

  const handlePasswordChange = (event) => {
    setPassword(event.target.value);
  };

  const handleUserCheckboxChange = (event) => {
    setIsUser(true);
    setGroup("Tracked");
  };

  const handleAttendantCheckboxChange = (event) => {
    setIsUser(false);
    setGroup("Attendant");
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
          history.push("/attendant");
          history.go(0);
        } else {
          history.push("/user");
          history.go(0);
        }
      })
      .catch((error) => {
        console.log(error);
        setError("Invalid credentials. Please try again.");
      });
  };

  const handleRegistration = (event) => {
    history.push("/register");
    history.go(0);
  };

  return (
    <form onSubmit={handleSubmit}>
      <div style={styles.login}>
        <div style={styles.username}>
          <div>
            <label htmlFor="username">UCID:</label>
            <input
              type="text"
              id="username"
              value={username}
              onChange={handleUsernameChange}
              style={styles.input}
            />
          </div>
          <div>
            <label htmlFor="password">Password:</label>
            <input
              type="password"
              id="password"
              value={password}
              onChange={handlePasswordChange}
              style={styles.input}
            />
          </div>
        </div>
        <div>
          <label htmlFor="user-checkbox">
            <input
              type="checkbox"
              id="user-checkbox"
              checked={isUser}
              onChange={handleUserCheckboxChange}
            />{" "}
            User
          </label>
          <label htmlFor="attendant-checkbox">
            <input
              type="checkbox"
              id="attendant-checkbox"
              checked={!isUser}
              onChange={handleAttendantCheckboxChange}
            />{" "}
            Attendant
          </label>
        </div>
        <div style={styles.errorMess}>{error}</div>
        <div>
          <button
            onClick={() => handleRegistration()}
            style={styles.buttonStyles}
          >
            Register
          </button>
          <button type="submit" style={styles.buttonStyles}>
            Login
          </button>
        </div>
      </div>
    </form>
  );
}

const styles = {
  buttonStyles: {
    width: "15%",
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
