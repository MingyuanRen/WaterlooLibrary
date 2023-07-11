import React, { useState } from "react";
import axios from "axios";
import styles from "./ViewUserInfo.module.css";

function ViewUserInfo() {
  const [email, setEmail] = useState("");
  const [userInfo, setUserInfo] = useState([]);
  const [error, setError] = useState("");
  const [editing, setEditing] = useState(null);

  const getUserInfo = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post("/admin/viewUserInfo", {
        email: email,
      });
      setError("");
      setUserInfo([response.data, ...userInfo]);
    } catch (err) {
      setError("User not found");
    }
  };

  const handleUpdate = async (index, user) => {
    try {
      const response = await axios.post("/admin/updateUserInfo", user);
      console.log(response.data); // 'success' if everything went well
      setEditing(null);
      setUserInfo(userInfo.map((item, i) => (i === index ? user : item)));
    } catch (err) {
      setError("Cannot intput empty attributes");
    }
  };

  return (
    <div>
      <form onSubmit={getUserInfo}>
        <input
          type="email"
          placeholder="Enter email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
        />
        <button type="submit">Get User Info</button>
      </form>
      {error && <div className={styles.error}>{error}</div>}
      {userInfo.map((user, index) => (
        <div key={index} className={styles.userInfo}>
          {editing === index ? (
            <>
              <div className={styles.editableFields}>
                <label>
                  Name:
                  <input
                    name="name"
                    value={user.name}
                    onChange={(e) =>
                      setUserInfo(
                        userInfo.map((item, i) =>
                          i === index ? { ...item, name: e.target.value } : item
                        )
                      )
                    }
                  />
                </label>
                <label>
                  Email:
                  <input
                    name="email"
                    value={user.email}
                    onChange={(e) =>
                      setUserInfo(
                        userInfo.map((item, i) =>
                          i === index
                            ? { ...item, email: e.target.value }
                            : item
                        )
                      )
                    }
                  />
                </label>
                <label>
                  Phone:
                  <input
                    name="phone"
                    value={user.phone}
                    onChange={(e) =>
                      setUserInfo(
                        userInfo.map((item, i) =>
                          i === index
                            ? { ...item, phone: e.target.value }
                            : item
                        )
                      )
                    }
                  />
                </label>
                {user.mid && (
                  <label>
                    Points:
                    <input
                      name="points"
                      value={user.points}
                      onChange={(e) =>
                        setUserInfo(
                          userInfo.map((item, i) =>
                            i === index
                              ? { ...item, points: e.target.value }
                              : item
                          )
                        )
                      }
                    />
                  </label>
                )}
                {user.mid && (
                  <label>
                    Start Date:
                    <input
                      name="start_date"
                      value={user.start_date}
                      onChange={(e) =>
                        setUserInfo(
                          userInfo.map((item, i) =>
                            i === index
                              ? { ...item, start_date: e.target.value }
                              : item
                          )
                        )
                      }
                    />
                  </label>
                )}
                {user.mid && (
                  <label>
                    End Date:
                    <input
                      name="end_date"
                      value={user.end_date}
                      onChange={(e) =>
                        setUserInfo(
                          userInfo.map((item, i) =>
                            i === index
                              ? { ...item, end_date: e.target.value }
                              : item
                          )
                        )
                      }
                    />
                  </label>
                )}
              </div>
              <button onClick={() => handleUpdate(index, user)}>
                Submit Update
              </button>
            </>
          ) : (
            <>
              <div className={styles.nonEditatbleFields}>
                <p>ID: {user.uid}</p>
                <p>Name: {user.name}</p>
                <p>Email: {user.email}</p>
                <p>Phone: {user.phone}</p>
                {user.mid && <p>Member ID: {user.mid}</p>}
                {user.mid && <p>Points: {user.points}</p>}
                {user.mid && <p>Membership Start Date: {user.start_date}</p>}
                {user.mid && <p>Membership End Date: {user.end_date}</p>}
                <button onClick={() => setEditing(index)}>Update Info</button>
              </div>
            </>
          )}
        </div>
      ))}
    </div>
  );
}

export default ViewUserInfo;
