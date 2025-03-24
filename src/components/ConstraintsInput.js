import React from "react";

const ConstraintsInput = ({ title, numRows, numVariables, values, setValues }) => {
  const initializeRow = (rowIndex) => {
    const updated = [...values];
    if (!updated[rowIndex]) {
      updated[rowIndex] = {
        coefficients: Array(numVariables).fill(""),
        operator: "<=",
        rhs: ""
      };
    }
    return updated;
  };

  const handleChange = (rowIndex, key, value) => {
    const updated = initializeRow(rowIndex);

    if (key === "operator" || key === "rhs") {
      updated[rowIndex][key] = value;
    } else {
      updated[rowIndex].coefficients[key] = value;
    }

    setValues([...updated]);
  };

  return (
    <div>
      <h2>{title}</h2>
      {Array.from({ length: numRows }).map((_, rowIndex) => (
        <div key={rowIndex}>
          {Array.from({ length: numVariables }).map((_, varIndex) => (
            <input
              key={varIndex}
              type="text"
              placeholder={`x${varIndex + 1}`}
              value={values[rowIndex]?.coefficients[varIndex] || ""}
              onChange={(e) => handleChange(rowIndex, varIndex, e.target.value)}
            />
          ))}
          <select
            value={values[rowIndex]?.operator || "="}
            onChange={(e) => handleChange(rowIndex, "operator", e.target.value)}
          >
            <option value="<=">≤</option>
            <option value=">=">≥</option>
            <option value="=">=</option>
          </select>
          <input
            type="text"
            placeholder="RHS"
            value={values[rowIndex]?.rhs || ""}
            onChange={(e) => handleChange(rowIndex, "rhs", e.target.value)}
          />
        </div>
      ))}
    </div>
  );
};

export default ConstraintsInput;
