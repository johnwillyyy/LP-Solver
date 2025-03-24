const NormalResults = ({ optimalValue, status, xValues, variableNames }) => {
    // Determine status color class
    const statusClass = status === "OPTIMAL" ? "status-optimal" : "status-nonoptimal";
  
    return (
      <>
        <div className="optimal-value-container">
        <div className="status">
            Status: <span className={`status-text ${statusClass}`}>{status}</span>
          </div>
          <div className="optimal-value">
            Optimal Value: <span className="optimal-value-text">{optimalValue}</span>
          </div>
        </div>
  
        <div className="solution-box">
          <p className="solution-title">Solution (X Values):</p>
          <div className="solution-values">
            {xValues.map((val, index) => (
              <span key={index} className="solution-item">
                {`${variableNames[index]} = ${val.toFixed(2)}`}
              </span>
            ))}
          </div>
        </div>
      </>
    );
  };
  
  export default NormalResults;
  