import React, { useState, useEffect } from "react";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from "recharts";
import axios from "axios";
import { Card, CardContent, Typography } from "@mui/material";
import classes from "./CaseStatusBar.module.css";

function CaseStatusBarChart() {
  const [caseCounts, setCaseCounts] = useState({
    Open: 0,
    Closed: 0,
    Pending: 0,
  });

  useEffect(() => {
    const fetchCaseCounts = async () => {
      try {
        const response = await axios.get(
          "http://localhost:8000/api/total-company-cases"
        );
        setCaseCounts(response.data);
      } catch (error) {
        console.error("Error fetching case counts:", error);
      }
    };
    fetchCaseCounts();
  }, []);

  const data = [
    {
      name: "Cases",
      Open: caseCounts.Open,
      Pending: caseCounts.Pending,
      Closed: caseCounts.Closed,
    },
  ];

  return (
    <>
      <h2 className={classes.title}>Total Number Of Cases In The Company</h2>
      <Card className={classes.card}>
        <CardContent className={classes.cardContent}>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart
              data={data}
              margin={{ top: 20, right: 30, left: 20, bottom: 5 }}
            >
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="name" />
              <YAxis />
              <Tooltip />
              <Legend />
              <Bar dataKey="Open" fill="#4caf50" />
              <Bar dataKey="Pending" fill="#e2c300" />
              <Bar dataKey="Closed" fill="#f44336" />
            </BarChart>
          </ResponsiveContainer>
        </CardContent>
      </Card>
    </>
  );
}

export default CaseStatusBarChart;
