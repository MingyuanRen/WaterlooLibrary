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
    <div className={styles.viewUserInfo_container}>
      {/* <div> */}
      <h1 className={styles.viewUserInfo_header}>View User Information</h1>
      <form onSubmit={getUserInfo} className={styles.viewUserInfo_form}>
        <input
          type="email"
          placeholder="Enter email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
        />
        <button type="submit">Get User Info</button>
      </form>
      {error && <div className={styles.viewUserInfo_error}>{error}</div>}
      {userInfo.map((user, index) => (
        <div key={index}>
          {editing === index ? (
            <>
              <div className={styles.viewUserInfo_editableFields}>
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
                <br></br>
                <button onClick={() => handleUpdate(index, user)}>
                  Submit Update
                </button>
                <hr></hr>
              </div>
            </>
          ) : (
            <>
              <div className={styles.viewUserInfo_nonEditatbleFields}>
                {/* <p> */}
                <span className={styles.viewUserInfo_infoSpan}>
                  <span className={styles.viewUserInfo_infoLabel}>ID: </span>{" "}
                  <span>{user.uid}</span>
                  {"     "}
                </span>
                <span className={styles.viewUserInfo_infoSpan}>
                  <span className={styles.viewUserInfo_infoLabel}>Name: </span>{" "}
                  <span>{user.name}</span>
                  {"     "}
                </span>
                <span className={styles.viewUserInfo_infoSpan}>
                  <span className={styles.viewUserInfo_infoLabel}>Email: </span>{" "}
                  <span>{user.email}</span>
                  {"     "}
                </span>
                <span className={styles.viewUserInfo_infoSpan}>
                  <span className={styles.viewUserInfo_infoLabel}>Phone: </span>{" "}
                  <span>{user.phone}</span>
                  {"     "}
                </span>

                {/* <span className={styles.viewUserInfo_infoLabel}>Name: {user.name}</span> {" "}
                <span className={styles.viewUserInfo_infoLabel}>Email: {user.email}</span> {" "}
                <span className={styles.viewUserInfo_infoLabel}>Phone: {user.phone}</span> {" "} */}
                {/* <span>Name: {user.name}</span> {"   "}
                <span>Email: {user.email}</span> {"   "}
                <span>Phone: {user.phone}</span> {"   "} */}
                {/* </p> */}
                <br></br>
                {user.mid && (
                  <span className={styles.viewUserInfo_infoSpan}>
                    <span className={styles.viewUserInfo_infoLabel}>
                      Member ID:{" "}
                    </span>{" "}
                    <span>{user.mid}</span>
                    {"     "}
                  </span>
                )}
                {user.mid && (
                  <span className={styles.viewUserInfo_infoSpan}>
                    <span className={styles.viewUserInfo_infoLabel}>
                      Points:{" "}
                    </span>{" "}
                    <span>{user.points}</span>
                    {"     "}
                  </span>
                )}
                {user.mid && (
                  <span className={styles.viewUserInfo_infoSpan}>
                    <span className={styles.viewUserInfo_infoLabel}>
                      Start Date:{" "}
                    </span>{" "}
                    <span>{user.start_date}</span>
                    {"     "}
                  </span>
                )}
                {user.mid && (
                  <span className={styles.viewUserInfo_infoSpan}>
                    <span className={styles.viewUserInfo_infoLabel}>
                      End Date:{" "}
                    </span>{" "}
                    <span>{user.end_date}</span>
                    {"     "}
                  </span>
                )}
                {user.mid && <br></br>}
                <button onClick={() => setEditing(index)}>Update Info</button>
                <hr></hr>
              </div>
            </>
          )}
        </div>
      ))}
    </div>
  );
}

export default ViewUserInfo;
