import uofc from "./ucinterlock_3c-CC.png";
import "./App.css";
import Login from "./LoginForm";
import AttendantPage from "./AttendantSheet";
import UserPage from "./UserSheet";
import RegisterPage from "./RegisterSheet";
import {
  BrowserRouter as Router,
  Switch,
  Route,
  useHistory,
} from "react-router-dom";
import React, { useLayoutEffect } from "react";
import ReactDOM from "react-dom";

function App() {
  const history = useHistory();

  return (
    <div
      className="App"
      style={{
        background: "linear-gradient(to bottom right, #E35335, #eb8100)",
        height: "100vh",
      }}
    >
      <div style={styles.container}>
        <div style={styles.header}>
          <img src={uofc} className="App-logo" alt="logo" style={styles.logo} />
          <h1 style={styles.title}>uTrack</h1>
        </div>
        <div>
          <h2 style={styles.desc}>
            Welcome to uTrack, your fitness center hour tracker for the
            University of Calgary!
          </h2>
        </div>
        <Router>
          <Switch>
            <Route exact path="/" component={Login} />
            <Route
              path="/attendant"
              render={() => <AttendantPage key={Math.random()} />}
            />
            <Route
              path="/user"
              render={() => <UserPage key={Math.random()} />}
            />
            <Route
              path="/register"
              render={() => <RegisterPage key={Math.random()} />}
            />
          </Switch>
        </Router>
      </div>
    </div>
  );
}

const styles = {
  container: {
    display: "flex",
    flexDirection: "column",
    alignItems: "center",
    justifyContent: "center",
  },
  header: {
    display: "flex",
    flexDirection: "row",
    alignItems: "center",
    justifyContent: "center",
    marginBottom: "30px",
    marginTop: "3%",
  },
  logo: {
    width: "80px",
    height: "80px",
    marginRight: "20px",
  },
  title: {
    color: "white",
    fontSize: "32px",
    fontWeight: "bold",
  },
  desc: {
    color: "white",
    fontSize: "16px",
    fontWeight: "normal",
    margin: 0,
  },
};

export default App;
