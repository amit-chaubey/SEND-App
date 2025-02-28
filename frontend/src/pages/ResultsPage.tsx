import React from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import { 
  Container, 
  Typography, 
  Button, 
  Box, 
  Card, 
  CardContent,
  CircularProgress,
  Paper
} from '@mui/material';
import { styled } from '@mui/material/styles';
import ReplayIcon from '@mui/icons-material/Replay';
import HomeIcon from '@mui/icons-material/Home';

interface ResultsState {
  score: number;
  totalRounds: number;
  focusSound: string;
}

const ScoreCircle = styled(Box)(({ theme }) => ({
  position: 'relative',
  display: 'inline-flex',
  margin: theme.spacing(4),
}));

const ResultsPage: React.FC = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const { score = 0, totalRounds = 10, focusSound = 'th' } = 
    location.state as ResultsState || {};
  
  const percentage = Math.round((score / totalRounds) * 100);
  
  const getFeedback = () => {
    if (percentage >= 90) return "Excellent! You're mastering this sound!";
    if (percentage >= 70) return "Great job! Keep practicing!";
    if (percentage >= 50) return "Good effort! You're making progress.";
    return "Keep practicing! You'll improve with time.";
  };

  const handlePlayAgain = () => {
    navigate('/game', { state: { focusSound } });
  };

  const handleGoHome = () => {
    navigate('/');
  };

  return (
    <Container maxWidth="md">
      <Box sx={{ my: 8, textAlign: 'center' }}>
        <Typography variant="h3" component="h1" gutterBottom>
          Your Results
        </Typography>
        
        <Paper elevation={3} sx={{ p: 4, mt: 4, backgroundColor: 'white' }}>
          <Typography variant="h5" color="textSecondary" gutterBottom>
            Sound: "{focusSound}"
          </Typography>
          
          <ScoreCircle>
            <CircularProgress 
              variant="determinate" 
              value={percentage} 
              size={200}
              thickness={5}
              color={percentage >= 70 ? "success" : percentage >= 50 ? "primary" : "error"}
            />
            <Box
              sx={{
                top: 0,
                left: 0,
                bottom: 0,
                right: 0,
                position: 'absolute',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
              }}
            >
              <Typography variant="h3" component="div" color="text.secondary">
                {percentage}%
              </Typography>
            </Box>
          </ScoreCircle>
          
          <Typography variant="h4" gutterBottom>
            Score: {score}/{totalRounds}
          </Typography>
          
          <Typography variant="h5" sx={{ my: 3 }}>
            {getFeedback()}
          </Typography>
          
          <Box sx={{ mt: 4, display: 'flex', justifyContent: 'center', gap: 2 }}>
            <Button 
              variant="contained" 
              color="primary" 
              size="large"
              startIcon={<ReplayIcon />}
              onClick={handlePlayAgain}
            >
              Play Again
            </Button>
            <Button 
              variant="outlined" 
              color="primary" 
              size="large"
              startIcon={<HomeIcon />}
              onClick={handleGoHome}
            >
              Home
            </Button>
          </Box>
        </Paper>
      </Box>
    </Container>
  );
};

export default ResultsPage; 