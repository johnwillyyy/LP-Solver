import React from 'react';

const Tableau = ({ tableau }) => {
  return (
    <div className="tableau-container">
      {tableau.note && <h3 className="tableau-note">{tableau.note}</h3>}
      <div className="tableau-wrapper">
        <table className="tableau">
          <thead>
            <tr className="tableau-header">
              <th className="tableau-cell">Basis</th>
              {tableau.columns.map((col, index) => (
                <th key={index} className="tableau-cell">{col}</th>
              ))}
            </tr>
          </thead>
          <tbody>
            {tableau.tableau.map((row, rowIndex) => (
              <tr key={rowIndex} className="tableau-row">
                <td className="tableau-cell basis-cell">
                  {tableau.rows[rowIndex]}
                </td>
                {row.map((cell, colIndex) => {
                  const formattedCell = parseFloat(cell);
                  const cellString = formattedCell.toString();
                  const decimalCount = cellString.includes('.') ? cellString.split('.')[1].length : 0;

                  // If the number has more than 5 decimals, truncate it to 5, otherwise, just display it as it is
                  const displayValue = decimalCount > 5 ? formattedCell.toFixed(5) : formattedCell;

                  return (
                    <td key={colIndex} className="tableau-cell">
                      {displayValue}
                    </td>
                  );
                })}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default Tableau;