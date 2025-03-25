import React from "react";
import ConstraintsInput from "./ConstraintsInput";

const GoalProgrammingSection = ({
  numGoals,
  numVariables,
  goals,
  setGoals,
  goalPriorities,
  setGoalPriorities,
  goalType,
  setGoalType,
  goalWeights,
  setGoalWeights
}) => {

  const handleWeightsChange = (index, value) => {
    const updated = [...goalWeights];
    updated[index] = parseFloat(value); // Convert input value to a number
    setGoalWeights(updated);
  };

  const handlePriorities = (index, value) => {
    const updated = [...goalPriorities];
    updated[index] = value;

    const parsed = updated.map(val => val ? parseInt(val) : null);
    const ranks = Array(numGoals).fill(0);

    parsed.forEach((val, inputIndex) => {
      if (val && val >= 1 && val <= numGoals) {
        ranks[val - 1] = inputIndex + 1;
      }
    });

    setGoalPriorities(ranks);
  };

  return (
    <div>
      <ConstraintsInput
        title="Goal Equations"
        numRows={numGoals}
        numVariables={numVariables}
        values={goals}
        setValues={setGoals}
      />

      <h2>Goal Prioritization</h2>

      <label>
        Goal Type:
        <select value={goalType} onChange={(e) => setGoalType(e.target.value)}>
          <option value="weights">Weights</option>
          <option value="priorities">Priorities</option>
        </select>
      </label>

      {goalType === "weights" && (
        <div>
          <h4>Goal Weights</h4>
          {Array.from({ length: numGoals }).map((_, goalIndex) => (
            <input
              key={goalIndex}
              type="number"
              placeholder={`Weight for Goal ${goalIndex + 1}`}
              value={goalWeights[goalIndex] || ''} // Show empty if undefined
              onChange={(e) => handleWeightsChange(goalIndex, e.target.value)}
            />
          ))}
        </div>
      )}


      {/* Goal Priorities (if Goal Type is "priorities") */}
      {goalType === "priorities" && (
        <div>
          <h4>Goal Priorities</h4>
          {Array.from({ length: numGoals }).map((_, goalIndex) => (
            <React.Fragment key={goalIndex}>
              <input
                type="number"
                min="1"
                max={numGoals}
                placeholder={`Priority for Goal ${goalIndex + 1}`}
                value={goalPriorities[goalIndex] || ''}
                onChange={(e) => handlePriorities(goalIndex, e.target.value)}
              />
              {goalIndex < numGoals - 1 && <span style={{ margin: "0 10px" }}>&gt;</span>}
            </React.Fragment>
          ))}
        </div>
      )}
    </div>
  );
};

export default GoalProgrammingSection;
