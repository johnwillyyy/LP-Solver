import React from "react";

const ObjectiveFunction = ({
  numVariables,
  objectiveType,
  setObjectiveType,
  objectiveCoefficients,
  setObjectiveCoefficients
}) => {
  const handleChange = (index, value) => {
    const updated = [...objectiveCoefficients];
    updated[index] = value;
    setObjectiveCoefficients(updated);
  };

  return (
    <div>
      <h2>Objective Function</h2>
      <select value={objectiveType} onChange={(e) => setObjectiveType(e.target.value)}>
        <option value="max">Maximize</option>
        <option value="min">Minimize</option>
      </select>
      <span> Z = </span>
      {Array.from({ length: numVariables }).map((_, index) => (
        <input
          key={index}
          type="text"
          placeholder={`x${index + 1}`}
          value={objectiveCoefficients[index] || ""}
          onChange={(e) => handleChange(index, e.target.value)}
        />
      ))}
    </div>
  );
};

export default ObjectiveFunction;
