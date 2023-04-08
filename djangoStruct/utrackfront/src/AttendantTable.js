import React, { useState, useEffect } from "react";
import axios from "axios";
import DatePickPopup from "./DatePickPopup";

function AttendantTable() {
  const [users, setUsers] = useState([]);
  const [selectedUser, setSelectedUser] = useState(null);

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
      {selectedUser && <DatePickPopup user={selectedUser} />}
    </div>
  );
}

export default AttendantTable;
