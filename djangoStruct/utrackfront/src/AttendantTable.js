import React, { useState, useEffect } from "react";
import axios from "axios";

function AttendantTable() {
  const [users, setUsers] = useState([]);

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

  const handleSelect = (row) => {
    // do something with the selected row
    console.log(row);
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
    </div>
  );
}

export default AttendantTable;
