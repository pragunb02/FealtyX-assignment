import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useSearchParams } from 'react-router-dom';
import './styles.css'; // Ensure you have styles in place for your components
import { Link } from 'react-router-dom';

const StudentList = () => {
  const [students, setStudents] = useState([]);
  const [totalPages, setTotalPages] = useState(0);
  const [currentPage, setCurrentPage] = useState(1);
  const [totalStudents, setTotalStudents] = useState(0);
  const [perPage, setPerPage] = useState(10);
  const [loadingSummary, setLoadingSummary] = useState(null); // Track which student is being summarized
  const [summaries, setSummaries] = useState({}); // Store summaries by student ID
  const [error, setError] = useState(null); // Error handling state
  const [loading, setLoading] = useState(true); // Loading state for the students list

  const [searchParams, setSearchParams] = useSearchParams();
  const page = searchParams.get('page') || 1;
  const per_page = searchParams.get('per_page') || perPage;

  // Fetch student data
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
        setStudents(response.data.students);
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

  // Fetch summary for a student
  const fetchSummary = async (id) => {
    setLoadingSummary(id);
    try {
      const response = await axios.get(`/students/${id}/summary`);
      setSummaries((prevSummaries) => ({
        ...prevSummaries,
        [id]: response.data.summary,
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

  // Handle page change
  const handlePageChange = (newPage) => {
    setSearchParams({ page: newPage, per_page: perPage });
  };

  return (
    <div className="container">
      <h1>Student List</h1>

      {/* Error message if any */}
      {error && <div className="error">{error}</div>}

      {/* Loading message while data is being fetched */}
      {loading ? (
        <div>Loading...</div>
      ) : (
        <ul className="student-list">
          {students.map((student) => (
            <li key={student.id}>
              <div>
                <Link to={`/students/${student.id}`}>{student.name}</Link>
                <button
                  onClick={() => fetchSummary(student.id)}
                  style={{
                    marginLeft: '10px',
                    background: '#3498db',
                    color: 'white',
                    padding: '5px 10px',
                    border: 'none',
                    borderRadius: '5px',
                    cursor: 'pointer',
                  }}
                >
                  {loadingSummary === student.id ? 'Generating Summary...' : 'View Summary'}
                </button>
              </div>

              {/* Summary Section */}
              <div className={`summary ${summaries[student.id] ? 'active' : ''}`}>
                {loadingSummary === student.id ? (
                  <div className="loading-spinner">
                    <span>Generating Summary...</span>
                    <div className="spinner"></div>
                  </div>
                ) : (
                  <p>{summaries[student.id]}</p>
                )}
              </div>
            </li>
          ))}
        </ul>
      )}

      {/* Pagination controls */}
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
