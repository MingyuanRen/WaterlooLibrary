import "./filter.css";

export const Filter = ({title, isActive, onClick}) => {
  return (
    <div
      className={"wrapper"}
      onClick={onClick}
      style={{ backgroundColor: `${isActive ? "lavender" : "white"}` }}
    >
      <div
        className={"circle"}
        style={{
          borderColor: `${
            title === "Title"
              ? "gold"
              : title === "Author"
              ? "tomato"
              : "limegreen"
          }`,
        }}
      ></div>
      <h3 className={"title"}>{title}</h3>
    </div>
    
  );
};

export const UserIcon = () => {
  // Add your icon SVG or image here
  return (
    <button className="user-icon-button">
      <svg xmlns="http://www.w3.org/2000/svg" data-name="Layer 1" viewBox="0 0 48 48" id="user"><path fill="#167ffc" d="M31.64,27.72a13.94,13.94,0,0,1-15.28,0A18,18,0,0,0,6.05,42.94a1,1,0,0,0,.27.75,1,1,0,0,0,.73.31H41a1,1,0,0,0,.73-.31,1,1,0,0,0,.27-.75A18,18,0,0,0,31.64,27.72Z" class="color42c3cf svgShape"></path><circle cx="24" cy="16" r="12" fill="#167ffc" class="color42c3cf svgShape"></circle></svg>
    </button>
  );
};
