import { useState } from "react";

function LoginForm() {
  const [ucid, setUcid] = useState("");
  const [password, setPassword] = useState("");
  const [isUser, setIsUser] = useState(true);

  const handleUcidChange = (event) => {
    setUcid(event.target.value);
  };

  const handlePasswordChange = (event) => {
    setPassword(event.target.value);
  };

  const handleUserCheckboxChange = (event) => {
    setIsUser(true);
  };

  const handleAttendantCheckboxChange = (event) => {
    setIsUser(false);
  };

  const handleSubmit = (event) => {
    event.preventDefault();
    // handle form submission here
  };

  return (
    <form onSubmit={handleSubmit}>
      <div style={styles.login}>
        <div style={styles.UCID}>
          <div>
            <label htmlFor="ucid">UCID:</label>
            <input
              type="text"
              id="ucid"
              value={ucid}
              onChange={handleUcidChange}
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
        <button type="submit">Login</button>
      </div>
    </form>
  );
}

const styles = {
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
    width: "300px",
    height: "250px",
  },
  UCID: {
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
