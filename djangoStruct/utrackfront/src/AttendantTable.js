import React, { useState, useEffect } from "react";
import axios from "axios";
import DatePickPopup from "./DatePickPopup";

function AttendantTable() {
  const [users, setUsers] = useState([]);
  const [selectedUser, setSelectedUser] = useState(null);
  const [showDatePicker, setShowDatePicker] = useState(false);
  const [disabled, setDisabled] = useState(false);
  const [checkInTime, setCheckInTime] = useState("");

  useEffect(() => {
    axios
      .get("http://127.0.0.1:8000/api/get_Users/")
      .then((response) => {
        setUsers(response.data);
        console.log(response.data);
      })
      .catch((error) => {
        console.log(error);
      });
  }, []);

  const handleSelect = (user) => {
    setSelectedUser(user);
    setShowDatePicker(true);

    axios
      .get(`http://127.0.0.1:8000/api/get_Checkins/last/${user.username}/`)
      .then((response) => {
        setDisabled(false);
        setCheckInTime(response.data.check_in_time);
        console.log(response.data.check_in_time);
        console.log(checkInTime);
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
      <h2>Attendant Name: John Doe</h2>
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
            <tr key={user.username}>
              <td>{user.username} </td>
              <td>{user.first_name}</td>
              <td>{user.last_name}</td>
              <td>
                <button onClick={() => handleSelect(user)}>Select</button>
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
        />
      )}
    </div>
  );
}

export default AttendantTable;
