import axios from "axios";
import { useHistory, useLocation } from "react-router-dom";
import React, { useState, useEffect } from "react";

function ExecTable() {
  const [users, setUsers] = useState([]);
  const [selectedUser, setSelectedUser] = useState(null);
  const [showUserPicker, setShowUserPicker] = useState(false);
  const [disabled, setDisabled] = useState(false);
  const [checkInTime, setCheckInTime] = useState("");
  const [success, setSuccess] = useState("");
  const [failure, setFailure] = useState("");
  const [sessions, setSessions] = useState([]);
  const [noSessions, setNoSessions] = useState(false);
  let attendantName = "";

  const getFacilityName = (facilityId) => {
    const facility = facilities.find((f) => f.value === facilityId);
    return facility ? facility.name : "Unknown Facility";
  };

  const history = useHistory();
  const location = useLocation();

  const facilities = [
    { name: "Fitness Center", value: "1" },
    { name: "Aquatic Center", value: "2" },
    { name: "Racquet Center", value: "3" },
    { name: "Gymnastic Center", value: "4" },
    { name: "Bouldering Wall", value: "5" },
    { name: "Outdoor Center", value: "6" },
  ];

  useEffect(() => {
    axios
      .get("http://127.0.0.1:8000/api/get_Users/")
      .then((response) => {
        setUsers(response.data);
      })
      .catch((error) => {
        setFailure("Error getting users. Contact admin.");
      });
  }, []);

  const logoutFunction = () => {
    history.push("/");
    history.go(0);
  };

  const handleSelect = (user) => {
    setSelectedUser(user);
    axios
      .get(`http://127.0.0.1:8000/api/Checkins/?tracked_username=${user}`)
      .then((response) => {
        setNoSessions(false);
        setSessions(response.data);
      })
      .catch((error) => {
        setNoSessions(true);
      });
    setShowUserPicker(true);
  };

  const handleDatePickPopupClose = () => {
    setSelectedUser(null);
    setShowUserPicker(false);
  };

  return (
    <div
      style={{
        height: "400px",
        overflow: "scroll",
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
      }}
    >
      <h2>
        <span>Executive Name: </span>
        <span>Joe</span>
      </h2>
      <table style={{ tableLayout: "fixed" }}>
        <thead>
          <tr>
            <th Style={{ width: "100px" }}>UCID</th>
            <th Style={{ width: "100px" }}>First Name</th>
            <th Style={{ width: "100px" }}>Last Name</th>
            <th Style={{ width: "100px" }}>Select Info</th>
          </tr>
        </thead>
        <tbody>
          {users.map((user) => (
            <tr
              key={user.username}
              style={{
                color: user === selectedUser ? "green" : "white",
              }}
              onClick={() => handleSelect(user)}
            >
              <td>{user.username} </td>
              <td>{user.first_name}</td>
              <td>{user.last_name}</td>
              <td>
                <button
                  onClick={() => {
                    handleSelect(user.username);
                    setSuccess("");
                    setFailure("");
                  }}
                >
                  Select
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
      {showUserPicker && !noSessions ? (
        <table>
          <thead>
            <tr>
              <th style={{ padding: "0 50px" }}>Date</th>
              <th style={{ padding: "0 50px" }}>Facility</th>
              <th style={{ padding: "0 50px" }}>Hours</th>
            </tr>
          </thead>
          <tbody>
            {sessions.map((session) => (
              <tr key={session.tracked_username}>
                <td>{session.date}</td>
                <td>{getFacilityName(session.facility_id)}</td>
                <td>{session.time_in_facility}</td>
              </tr>
            ))}
          </tbody>
        </table>
      ) : showUserPicker && sessions.length === 0 ? (
        <div>No tracked sessions.</div>
      ) : null}
      <button
        onClick={() => {
          logoutFunction();
          setSuccess("");
          setFailure("");
          setSessions(null);
        }}
        style={{ marginTop: "1%", marginRight: "250px" }}
      >
        Logout
      </button>
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
        {failure}
      </div>
    </div>
  );
}

export default ExecTable;
