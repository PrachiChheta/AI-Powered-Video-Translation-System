import React, { useState } from 'react';
import { Upload, Languages, FileVideo, Loader2, CheckCircle2, AlertCircle } from 'lucide-react';

export default function VideoTranslationApp() {
  const [file, setFile] = useState(null);
  const [sourceLanguage, setSourceLanguage] = useState('English');
  const [targetLanguage, setTargetLanguage] = useState('Hindi');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  const languages = [
    'English', 'Hindi', 'Spanish', 'French', 'German', 'Chinese', 
    'Japanese', 'Korean', 'Arabic', 'Portuguese', 'Russian', 'Italian'
  ];

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    if (selectedFile && selectedFile.type.startsWith('video/')) {
      setFile(selectedFile);
      setError(null);
    } else {
      setError('Please select a valid video file');
      setFile(null);
    }
  };

  const handleSubmit = async () => {
    if (!file) {
      setError('Please select a video file');
      return;
    }

    setLoading(true);
    setError(null);
    setResult(null);

    const formData = new FormData();
    formData.append('file', file);
    formData.append('source_language', sourceLanguage);
    formData.append('target_language', targetLanguage);

    try {
      const response = await fetch('http://localhost:8000/api/translate-video', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error('Translation failed');
      }

      const data = await response.json();
      setResult(data);
    } catch (err) {
      setError(err.message || 'An error occurred during translation');
    } finally {
      setLoading(false);
    }
  };

  const styles = {
    container: {
      minHeight: '100vh',
      background: 'linear-gradient(135deg, #e0f2fe 0%, #c7d2fe 100%)',
      padding: '2rem',
      fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif'
    },
    mainCard: {
      maxWidth: '56rem',
      margin: '0 auto',
      backgroundColor: 'white',
      borderRadius: '1rem',
      boxShadow: '0 20px 25px -5px rgba(0, 0, 0, 0.1)',
      padding: '2rem'
    },
    header: {
      display: 'flex',
      alignItems: 'center',
      gap: '0.75rem',
      marginBottom: '2rem'
    },
    title: {
      fontSize: '1.875rem',
      fontWeight: 'bold',
      color: '#1f2937',
      margin: 0
    },
    label: {
      display: 'block',
      fontSize: '0.875rem',
      fontWeight: '500',
      color: '#374151',
      marginBottom: '0.5rem'
    },
    uploadArea: {
      position: 'relative',
      border: '2px dashed #d1d5db',
      borderRadius: '0.5rem',
      padding: '2rem',
      textAlign: 'center',
      cursor: 'pointer',
      transition: 'border-color 0.3s',
      marginBottom: '1.5rem'
    },
    uploadAreaHover: {
      borderColor: '#6366f1'
    },
    fileInput: {
      position: 'absolute',
      inset: 0,
      width: '100%',
      height: '100%',
      opacity: 0,
      cursor: 'pointer'
    },
    uploadText: {
      fontSize: '0.875rem',
      color: '#4b5563',
      margin: '0.75rem 0 0.25rem 0'
    },
    uploadSubtext: {
      fontSize: '0.75rem',
      color: '#6b7280',
      margin: 0
    },
    gridContainer: {
      display: 'grid',
      gridTemplateColumns: 'repeat(2, 1fr)',
      gap: '1rem',
      marginBottom: '1.5rem'
    },
    select: {
      width: '100%',
      padding: '0.5rem 1rem',
      border: '1px solid #d1d5db',
      borderRadius: '0.5rem',
      fontSize: '1rem',
      outline: 'none',
      transition: 'border-color 0.2s, box-shadow 0.2s'
    },
    button: {
      width: '100%',
      backgroundColor: '#4f46e5',
      color: 'white',
      padding: '0.75rem 1.5rem',
      borderRadius: '0.5rem',
      fontWeight: '500',
      border: 'none',
      cursor: 'pointer',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      gap: '0.5rem',
      fontSize: '1rem',
      transition: 'background-color 0.3s'
    },
    buttonDisabled: {
      backgroundColor: '#9ca3af',
      cursor: 'not-allowed'
    },
    errorBox: {
      marginTop: '1.5rem',
      backgroundColor: '#fef2f2',
      border: '1px solid #fecaca',
      borderRadius: '0.5rem',
      padding: '1rem',
      display: 'flex',
      gap: '0.75rem'
    },
    errorTitle: {
      fontSize: '0.875rem',
      fontWeight: '500',
      color: '#991b1b',
      margin: '0 0 0.25rem 0'
    },
    errorText: {
      fontSize: '0.875rem',
      color: '#b91c1c',
      margin: 0
    },
    successBox: {
      marginTop: '1.5rem',
      backgroundColor: '#f0fdf4',
      border: '1px solid #bbf7d0',
      borderRadius: '0.5rem',
      padding: '1.5rem'
    },
    successHeader: {
      display: 'flex',
      alignItems: 'center',
      gap: '0.5rem',
      marginBottom: '1rem'
    },
    successTitle: {
      fontSize: '1.125rem',
      fontWeight: '600',
      color: '#166534',
      margin: 0
    },
    transcriptBox: {
      backgroundColor: 'white',
      borderRadius: '0.5rem',
      padding: '1rem',
      marginBottom: '1rem'
    },
    transcriptTitle: {
      fontWeight: '500',
      color: '#374151',
      marginBottom: '0.5rem'
    },
    transcriptContent: {
      fontSize: '0.875rem',
      color: '#4b5563',
      whiteSpace: 'pre-wrap',
      maxHeight: '12rem',
      overflowY: 'auto',
      backgroundColor: '#f9fafb',
      padding: '0.75rem',
      borderRadius: '0.25rem',
      fontFamily: 'monospace'
    },
    footer: {
      marginTop: '1.5rem',
      textAlign: 'center',
      fontSize: '0.875rem',
      color: '#4b5563'
    }
  };

  return (
    <div style={styles.container}>
      <div style={styles.mainCard}>
        <div style={styles.header}>
          <FileVideo style={{ width: '2.5rem', height: '2.5rem', color: '#4f46e5' }} />
          <h1 style={styles.title}>Video Translation Tool</h1>
        </div>

        <div>
          <div>
            <label style={styles.label}>Upload Video File</label>
            <div style={styles.uploadArea}>
              <input
                type="file"
                accept="video/*"
                onChange={handleFileChange}
                style={styles.fileInput}
              />
              <Upload style={{ width: '3rem', height: '3rem', color: '#9ca3af', margin: '0 auto' }} />
              <p style={styles.uploadText}>
                {file ? file.name : 'Click to upload or drag and drop'}
              </p>
              <p style={styles.uploadSubtext}>MP4, AVI, MOV, etc.</p>
            </div>
          </div>

          <div style={styles.gridContainer}>
            <div>
              <label style={styles.label}>Source Language</label>
              <select
                value={sourceLanguage}
                onChange={(e) => setSourceLanguage(e.target.value)}
                style={styles.select}
              >
                {languages.map((lang) => (
                  <option key={lang} value={lang}>{lang}</option>
                ))}
              </select>
            </div>

            <div>
              <label style={styles.label}>Target Language</label>
              <select
                value={targetLanguage}
                onChange={(e) => setTargetLanguage(e.target.value)}
                style={styles.select}
              >
                {languages.map((lang) => (
                  <option key={lang} value={lang}>{lang}</option>
                ))}
              </select>
            </div>
          </div>

          <button
            onClick={handleSubmit}
            disabled={loading || !file}
            style={{...styles.button, ...(loading || !file ? styles.buttonDisabled : {})}}
            onMouseEnter={(e) => !loading && file && (e.target.style.backgroundColor = '#4338ca')}
            onMouseLeave={(e) => !loading && file && (e.target.style.backgroundColor = '#4f46e5')}
          >
            {loading ? (
              <>
                <Loader2 style={{ width: '1.25rem', height: '1.25rem', animation: 'spin 1s linear infinite' }} />
                Processing...
              </>
            ) : (
              <>
                <Languages style={{ width: '1.25rem', height: '1.25rem' }} />
                Translate Video
              </>
            )}
          </button>
        </div>

        {error && (
          <div style={styles.errorBox}>
            <AlertCircle style={{ width: '1.25rem', height: '1.25rem', color: '#dc2626', flexShrink: 0 }} />
            <div>
              <p style={styles.errorTitle}>Error</p>
              <p style={styles.errorText}>{error}</p>
            </div>
          </div>
        )}

        {result && (
          <div style={styles.successBox}>
            <div style={styles.successHeader}>
              <CheckCircle2 style={{ width: '1.5rem', height: '1.5rem', color: '#16a34a' }} />
              <h3 style={styles.successTitle}>Translation Complete!</h3>
            </div>
            
            <div>
              <div style={styles.transcriptBox}>
                <h4 style={styles.transcriptTitle}>Original Transcript:</h4>
                <pre style={styles.transcriptContent}>{result.original_transcript}</pre>
              </div>

              <div style={styles.transcriptBox}>
                <h4 style={styles.transcriptTitle}>Translated Transcript:</h4>
                <pre style={styles.transcriptContent}>{result.translated_transcript}</pre>
              </div>
            </div>
          </div>
        )}
      </div>

      <div style={styles.footer}>
        <p>Powered by Whisper AI & OpenAI Translation</p>
      </div>
    </div>
  );
}