import React, { useState, useEffect } from "react";
import axios from "axios";
import DatePickPopup from "./DatePickPopup";
import { useHistory, useLocation } from "react-router-dom";

function AttendantTable() {
  const [users, setUsers] = useState([]);
  const [selectedUser, setSelectedUser] = useState(null);
  const [showDatePicker, setShowDatePicker] = useState(false);
  const [disabled, setDisabled] = useState(false);
  const [checkInTime, setCheckInTime] = useState("");
  const [success, setSuccess] = useState("");
  const [failure, setFailure] = useState("");
  let attendantName = "";

  const history = useHistory();
  const location = useLocation();
  attendantName = location.state.params;

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
    setShowDatePicker(true);

    axios
      .get(`http://127.0.0.1:8000/api/Checkout/last/${user.username}/`)
      .then((response) => {
        setDisabled(false);
        setCheckInTime(response.data.check_in_time);
      })
      .catch((error) => {
        setDisabled(true);
      });
  };

  const handleDatePickPopupClose = () => {
    setSelectedUser(null);
    setShowDatePicker(false);
  };

  return (
    <div>
      <h2>
        <span>Attendant Name: </span>
        <span>{attendantName}</span>
      </h2>
      <table>
        <thead>
          <tr>
            <th>UCID</th>
            <th>First Name</th>
            <th>Last Name</th>
            <th>Select Info</th>
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
                    handleSelect(user);
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
      {showDatePicker && (
        <DatePickPopup
          user={selectedUser}
          handleClose={handleDatePickPopupClose}
          disabled={disabled}
          checkInTime={checkInTime}
          setFailure={setFailure}
          setSuccess={setSuccess}
        />
      )}
      <button
        onClick={() => {
          logoutFunction();
          setSuccess("");
          setFailure("");
        }}
        style={{ marginTop: "1%", marginRight: "300px" }}
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

export default AttendantTable;
