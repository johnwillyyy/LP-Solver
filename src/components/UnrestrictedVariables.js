import React from "react";

const UnrestrictedVariables = ({ numVariables, unrestrictedVariables, setUnrestrictedVariables }) => {
  const handleChange = (value) => {
    setUnrestrictedVariables((prev) =>
      prev.includes(value)
        ? prev.filter((v) => v !== value)
        : [...prev, value]
    );
  };

  return (
    <div>
      <h2>Select Unrestricted Variables</h2>
      {Array.from({ length: numVariables }).map((_, index) => (
        <label key={index} style={{ marginRight: "10px" }}>
          <input
            type="checkbox"
            value={index}
            onChange={(e) => handleChange(e.target.value)}
            checked={unrestrictedVariables.includes(index.toString())}
          />
          {` x${index + 1}`}
        </label>
      ))}
    </div>
  );
};

export default UnrestrictedVariables;
