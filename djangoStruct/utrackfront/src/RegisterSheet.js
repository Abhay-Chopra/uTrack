import React, { useState } from "react";
import axios from "axios";
import { useHistory } from "react-router-dom";
function LoginForm() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [firstName, setFirstName] = useState("");
  const [lastName, setLastName] = useState("");
  const [email, setEmail] = useState("");
  const [group, setGroup] = useState("Tracked");
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");
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

    if (
      username === "" ||
      password === "" ||
      email === "" ||
      firstName === "" ||
      lastName === ""
    ) {
      setError("Make sure all fields are appropriately filled in.");
    } else {
      axios
        .post("http://127.0.0.1:8000/api/auth/register/", {
          username,
          password,
          email,
          group,
          first_name: firstName,
          last_name: lastName,
        })
        .then((response) => {
          setSuccess("Validation complete. You may now login.");
          setUsername("");
          setPassword("");
          setFirstName("");
          setLastName("");
          setEmail("");
        })
        .catch((error) => {
          setError("Make sure all fields are appropriately filled in.");
        });
    }
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
            <label htmlFor="first_name">First Name:</label>
            <input
              type="text"
              id="first_name"
              value={firstName}
              onChange={(event) => setFirstName(event.target.value)}
              style={styles.input}
            />
          </div>
          <div>
            <label htmlFor="last_name">Last Name:</label>
            <input
              type="text"
              id="last_name"
              value={lastName}
              onChange={(event) => setLastName(event.target.value)}
              style={styles.input}
            />
          </div>
          <div>
            <label htmlFor="email">Email:</label>
            <input
              type="email"
              id="email"
              value={email}
              onChange={(event) => setEmail(event.target.value)}
              style={styles.input}
            />
          </div>
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
        <div>
          <button
            onClick={() => {
              handleLogout();
              setError("");
              setSuccess("");
            }}
            style={styles.buttonStyles}
          >
            Back
          </button>
          <button
            type="submit"
            style={styles.buttonStyles}
            onClick={() => {
              setError("");
              setSuccess("");
            }}
          >
            Create
          </button>
        </div>
        <div
          style={{
            fontSize: "15px",
            color: "green",
          }}
        >
          {success}
        </div>
        <div
          style={{
            fontSize: "15px",
            color: "red",
          }}
        >
          {error}
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
    height: "400px",
    overflow: "scroll",
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
