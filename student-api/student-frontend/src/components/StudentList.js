import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useSearchParams } from 'react-router-dom';
import { Link } from 'react-router-dom';
import './StudentList.css';

const StudentList = () => {
  const [students, setStudents] = useState([]);
  const [totalPages, setTotalPages] = useState(0);
  const [totalStudents, setTotalStudents] = useState(0);
  const [perPage, setPerPage] = useState(10);
  const [loadingSummary, setLoadingSummary] = useState(null);
  const [summaries, setSummaries] = useState({});
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(true);
  const [toggledSummaries, setToggledSummaries] = useState({});

  const [searchParams, setSearchParams] = useSearchParams();
  const page = searchParams.get('page') || 1;
  const per_page = searchParams.get('per_page') || perPage;

  useEffect(() => {
    const fetchStudents = async () => {
      setLoading(true);
      setError(null);
      try {
        const response = await axios.get('/students', {
          params: {
            page: page,
            per_page: per_page,
          },
        });
        const fetchedStudents = response.data.students;
        if (fetchedStudents.length === 0) {
          localStorage.setItem('students', 'No Students');
        }
        setStudents(fetchedStudents);
        setTotalPages(response.data.total_pages);
        setTotalStudents(response.data.total);
      } catch (error) {
        setError('Error fetching student data.');
      } finally {
        setLoading(false);
      }
    };

    fetchStudents();
  }, [page, per_page]);

  const formatSummary = (summary) => {
    if (!summary) return '';
    const cleanedSummary = summary.replace(/\*\*/g, '').replace(/\n/g, ' ');
    const summaryLines = cleanedSummary.split(/[0-9]\.\s+/).filter(line => line.trim());
    const formattedSummary = summaryLines.map((point, index) => `${index + 1}. ${point.trim()}`).join('\n');
    return formattedSummary;
  };

  const fetchSummary = async (id) => {
    setLoadingSummary(id);
    try {
      const response = await axios.get(`/students/${id}/summary`);
      const cleanedSummary = formatSummary(response.data.summary);
      setSummaries((prevSummaries) => ({
        ...prevSummaries,
        [id]: cleanedSummary,
      }));
    } catch (error) {
      setSummaries((prevSummaries) => ({
        ...prevSummaries,
        [id]: 'Failed to generate summary.',
      }));
    } finally {
      setLoadingSummary(null);
    }
  };

  const toggleSummary = (id) => {
    setToggledSummaries((prevToggledSummaries) => ({
      ...prevToggledSummaries,
      [id]: !prevToggledSummaries[id],
    }));

    if (!summaries[id]) {
      fetchSummary(id);
    }
  };

  const handlePageChange = (newPage) => {
    setSearchParams({ page: newPage, per_page: perPage });
  };

  return (
    <div className="container">
      <h1>Student List</h1>

      {error && <div className="error">{error}</div>}

      {loading ? (
        <div>Loading...</div>
      ) : students.length === 0 ? (
        <div>No Students Available</div>
      ) : (
        <ul className="student-list">
          {students.map((student) => (
            <li key={student.id}>
              <div>
                <Link to={`/students/${student.id}`}>{student.name}</Link>
                <button
                  onClick={() => toggleSummary(student.id)}
                  style={{
                    marginLeft: '10px',
                    background: toggledSummaries[student.id] ? '#e74c3c' : '#3498db',
                    color: 'white',
                    padding: '5px 10px',
                    border: 'none',
                    borderRadius: '5px',
                    cursor: 'pointer',
                  }}
                >
                  {toggledSummaries[student.id] ? 'Hide Summary' : 'View Summary'}
                </button>
              </div>

              {toggledSummaries[student.id] && (
                <div className="summary" style={{ marginTop: '10px' }}>
                  {loadingSummary === student.id ? (
                    <div className="loading-spinner">
                      <span>Generating Summary...</span>
                      <div className="spinner"></div>
                    </div>
                  ) : (
                    <pre style={summaryStyle}>{summaries[student.id]}</pre>
                  )}
                </div>
              )}
            </li>
          ))}
        </ul>
      )}

      <div className="pagination">
        {page > 1 && (
          <button onClick={() => handlePageChange(parseInt(page) - 1)} disabled={page <= 1}>
            Previous
          </button>
        )}
        {page < totalPages && (
          <button onClick={() => handlePageChange(parseInt(page) + 1)} disabled={page >= totalPages}>
            Next
          </button>
        )}
      </div>
    </div>
  );
};

export default StudentList;

const summaryStyle = {
  maxHeight: '150px',
  overflowY: 'auto',
  padding: '10px',
  border: '1px solid #ccc',
  backgroundColor: '#f9f9f9',
  fontSize: '14px',
  lineHeight: '1.5',
  whiteSpace: 'pre-wrap',
  borderRadius: '5px',
};
