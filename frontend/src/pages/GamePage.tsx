import React, { useState, useEffect, useRef } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import { 
  Container, 
  Typography, 
  Button, 
  Box, 
  Paper,
  TextField,
  IconButton,
  LinearProgress,
  CircularProgress
} from '@mui/material';
import VolumeUpIcon from '@mui/icons-material/VolumeUp';
import CheckIcon from '@mui/icons-material/Check';
import CloseIcon from '@mui/icons-material/Close';
import axios from 'axios';

// Replace hardcoded localhost URL with environment variable
const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

// Fallback words if API fails
const wordsBySounds: Record<string, string[]> = {
  'th': ['think', 'three', 'thumb', 'thrill', 'thunder', 'thief', 'theater', 'thousand', 'thread', 'throne'],
  'sh': ['ship', 'wish', 'shop', 'shine', 'shower', 'shell', 'shadow', 'share', 'sharp', 'sheep'],
  'ch': ['chair', 'watch', 'church', 'cheese', 'chicken', 'chocolate', 'champion', 'children', 'cherry', 'beach'],
  'ph': ['phone', 'graph', 'photo', 'phrase', 'dolphin', 'elephant', 'alphabet', 'pharmacy', 'physics', 'nephew'],
  'wh': ['what', 'when', 'where', 'which', 'whale', 'wheel', 'whisper', 'whistle', 'white', 'whip'],
  'ng': ['sing', 'ring', 'king', 'strong', 'wrong', 'tongue', 'swing', 'bring', 'wing', 'song'],
};

const GamePage: React.FC = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const { focusSound } = location.state || { focusSound: 'sh' }; // Default to 'sh' if not specified
  
  const [currentRound, setCurrentRound] = useState(1);
  const [score, setScore] = useState(0);
  const [currentWord, setCurrentWord] = useState('');
  const [userInput, setUserInput] = useState('');
  const [showWord, setShowWord] = useState(false);
  const [gameStatus, setGameStatus] = useState<'playing' | 'correct' | 'incorrect' | 'finished'>('playing');
  const [difficulty, setDifficulty] = useState<'Easy' | 'Medium' | 'Hard'>('Easy');
  const [wordsByDifficulty, setWordsByDifficulty] = useState<Record<string, string[]>>({
    'Easy': [],
    'Medium': [],
    'Hard': []
  });
  const [usedWords, setUsedWords] = useState<Set<string>>(new Set());
  const [isLoading, setIsLoading] = useState(false);
  
  // Add new state for timer
  const [wordTimer, setWordTimer] = useState<number>(5);
  const [isTimerActive, setIsTimerActive] = useState(false);
  const timerRef = useRef<NodeJS.Timeout>();
  
  const totalRounds = 10;
  
  // Add a loading ref to prevent duplicate requests
  const loadingRef = useRef(false);
  
  // Fetch words for the selected sound and categorize by difficulty
  useEffect(() => {
    const fetchWords = async () => {
      // If already loading, skip
      if (loadingRef.current) return;
      
      loadingRef.current = true;
      setIsLoading(true);
      
      try {
        console.log('Fetching words for sound:', focusSound);
        const response = await axios.get(`${API_URL}/api/words-by-sound?sound=${focusSound}&count=50`, {
          headers: {
            'Cache-Control': 'no-cache',
            'Pragma': 'no-cache'
          }
        });
        
        const words = response.data.words;
        
        // Categorize words by difficulty (length is a simple proxy for difficulty)
        const easy: string[] = [];
        const medium: string[] = [];
        const hard: string[] = [];
        
        words.forEach((word: string) => {
          if (word.length <= 4) {
            easy.push(word);
          } else if (word.length <= 7) {
            medium.push(word);
          } else {
            hard.push(word);
          }
        });
        
        setWordsByDifficulty({
          'Easy': easy.length >= 10 ? easy : [...easy, ...medium].slice(0, 10),
          'Medium': medium.length >= 10 ? medium : [...medium, ...hard, ...easy].slice(0, 10),
          'Hard': hard.length >= 10 ? hard : [...hard, ...medium].slice(0, 10)
        });
      } catch (error) {
        console.error('Error details:', error);
        // Use fallback words
        const fallbackWords = wordsBySounds[focusSound] || [];
        console.log('Using fallback words:', fallbackWords);
        setWordsByDifficulty({
          'Easy': fallbackWords.filter(w => w.length <= 4),
          'Medium': fallbackWords.filter(w => w.length > 4 && w.length <= 7),
          'Hard': fallbackWords.filter(w => w.length > 7)
        });
      } finally {
        setIsLoading(false);
        loadingRef.current = false;
      }
    };
    
    if (focusSound) {
      fetchWords();
    }
    
    return () => {
      loadingRef.current = false;
    };
  }, [focusSound]);
  
  // When difficulty changes, reset the game
  useEffect(() => {
    if (currentRound > 1) {
      restartGame();
    }
  }, [difficulty]);
  
  // Select a new word based on current difficulty
  const selectNewWord = () => {
    const availableWords = wordsByDifficulty[difficulty].filter(word => !usedWords.has(word));
    
    if (availableWords.length === 0) {
      // Reset used words and try again
      setUsedWords(new Set());
      const allWords = wordsByDifficulty[difficulty];
      const randomIndex = Math.floor(Math.random() * allWords.length);
      const newWord = allWords[randomIndex];
      setCurrentWord(newWord);
      return true;
    }
    
    const randomIndex = Math.floor(Math.random() * availableWords.length);
    const newWord = availableWords[randomIndex];
    setCurrentWord(newWord);
    
    setUsedWords(prev => new Set(Array.from(prev).concat([newWord])));
    return true;
  };
  
  // Add this useEffect to initialize the first word
  useEffect(() => {
    if (wordsByDifficulty[difficulty].length > 0 && !currentWord) {
      selectNewWord();
    }
  }, [wordsByDifficulty, difficulty]);
  
  const playSound = () => {
    if (!currentWord) return;
    
    if ('speechSynthesis' in window) {
      try {
        window.speechSynthesis.cancel();
        
        const utterance = new SpeechSynthesisUtterance(currentWord);
        utterance.rate = 0.8;
        
        // Clear existing timer
        if (timerRef.current) {
          clearInterval(timerRef.current);
        }
        
        // Show word and start timer
        setShowWord(true);
        setWordTimer(5);
        setIsTimerActive(true);
        
        timerRef.current = setInterval(() => {
          setWordTimer(prev => {
            if (prev <= 1) {
              clearInterval(timerRef.current);
              setShowWord(false);
              setIsTimerActive(false);
              return 0;
            }
            return prev - 1;
          });
        }, 1000);
        
        window.speechSynthesis.speak(utterance);
      } catch (error) {
        console.error('Speech synthesis error:', error);
        // Show error message to user
        alert('Speech synthesis failed. Please try again.');
      }
    } else {
      alert('Speech synthesis is not supported in your browser.');
    }
  };
  
  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setUserInput(e.target.value);
  };
  
  const checkAnswer = () => {
    if (!currentWord || showWord) return;
    
    if (userInput.toLowerCase().trim() === currentWord.toLowerCase()) {
      setScore(score + 1);
      setGameStatus('correct');
    } else {
      setGameStatus('incorrect');
    }
    
    // Move to next round after a delay
    setTimeout(() => {
      if (currentRound < totalRounds) {
        setCurrentRound(currentRound + 1);
        setUserInput('');
        setGameStatus('playing');
        selectNewWord();
      } else {
        setGameStatus('finished');
      }
    }, 1500);
  };
  
  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && userInput && !showWord) {
      checkAnswer();
    }
  };
  
  const restartGame = () => {
    setCurrentRound(1);
    setScore(0);
    setGameStatus('playing');
    setUsedWords(new Set());
  };
  
  const goHome = () => {
    navigate('/');
  };
  
  const handleDifficultyChange = (newDifficulty: 'Easy' | 'Medium' | 'Hard') => {
    if (difficulty !== newDifficulty) {
      setDifficulty(newDifficulty);
    }
  };
  
  // Cleanup timer on unmount or when word changes
  useEffect(() => {
    return () => {
      if (timerRef.current) {
        clearInterval(timerRef.current);
      }
    };
  }, [currentWord]);
  
  // useEffect at the top level of the component
  useEffect(() => {
    if (wordsByDifficulty[difficulty].length > 0) {
      selectNewWord();
    }
  }, [wordsByDifficulty, difficulty]); // This will run when words are loaded or difficulty changes
  
  return (
    <Container maxWidth="lg">
      <Box sx={{ my: 4 }}>
        <Typography variant="h3" component="h1" gutterBottom>
          Sound: "{focusSound}"
        </Typography>
        
        <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 2 }}>
          <Button 
            variant="contained" 
            color="primary"
            onClick={goHome}
          >
            Back to Home
          </Button>
          
          <Box>
            <Typography variant="h6" component="span" sx={{ mr: 2 }}>
              Score: {score}/{totalRounds}
            </Typography>
            <Typography variant="h6" component="span">
              Round: {currentRound}/{totalRounds}
            </Typography>
            {/* <IconButton onClick={() => {}} sx={{ ml: 2 }}>
              <PauseIcon />
            </IconButton> */}
          </Box>
        </Box>
        
        <LinearProgress 
          variant="determinate" 
          value={(currentRound / totalRounds) * 100} 
          sx={{ mb: 4, height: 10, borderRadius: 5 }}
        />
        
        {isLoading && (
          <LinearProgress sx={{ mb: 2 }} />
        )}
        
        <Paper elevation={3} sx={{ p: 4, mb: 4, display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
          {gameStatus === 'finished' ? (
            <Box textAlign="center">
              <Typography variant="h4" gutterBottom>
                Game Finished!
              </Typography>
              <Typography variant="h5" gutterBottom>
                Your final score: {score}/{totalRounds}
              </Typography>
              <Box sx={{ mt: 3 }}>
                <Button variant="contained" color="primary" onClick={restartGame} sx={{ mr: 2 }}>
                  Play Again
                </Button>
                <Button variant="outlined" onClick={goHome}>
                  Return Home
                </Button>
              </Box>
            </Box>
          ) : (
            <>
              <IconButton 
                onClick={playSound} 
                sx={{ fontSize: '4rem', mb: 3 }}
                color="primary"
              >
                <VolumeUpIcon fontSize="inherit" />
              </IconButton>
              
              {showWord && (
                <Box sx={{ 
                  position: 'relative', 
                  display: 'flex', 
                  alignItems: 'center', 
                  justifyContent: 'center',
                  gap: 4,
                  mb: 3
                }}>
                  <Typography variant="h4">
                    {currentWord}
                  </Typography>
                  
                  <Box sx={{ 
                    position: 'relative',
                    width: 60,
                    height: 60,
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center'
                  }}>
                    <CircularProgress
                      variant="determinate"
                      value={(wordTimer / 5) * 100}
                      size={60}
                      thickness={4}
                      sx={{
                        position: 'absolute',
                        color: 'primary.main'
                      }}
                    />
                    <Typography variant="h6" color="primary">
                      {wordTimer}
                    </Typography>
                  </Box>
                </Box>
              )}
              
              <Box sx={{ width: '100%', maxWidth: 500, mt: 3 }}>
                <TextField
                  fullWidth
                  label="Type the word you heard"
                  variant="outlined"
                  value={userInput}
                  onChange={handleInputChange}
                  onKeyDown={handleKeyPress}
                  disabled={gameStatus === 'correct' || gameStatus === 'incorrect' || showWord}
                  autoFocus
                  sx={{ backgroundColor: 'white' }}
                />
                
                <Button
                  variant="contained"
                  color="primary"
                  fullWidth
                  sx={{ mt: 2 }}
                  onClick={checkAnswer}
                  disabled={!userInput || showWord || gameStatus === 'correct' || gameStatus === 'incorrect'}
                >
                  Submit
                </Button>
              </Box>
              
              {gameStatus === 'correct' && (
                <Box sx={{ mt: 3, display: 'flex', alignItems: 'center', color: 'success.main' }}>
                  <CheckIcon />
                  <Typography variant="h6" sx={{ ml: 1 }}>
                    Correct!
                  </Typography>
                </Box>
              )}
              
              {gameStatus === 'incorrect' && (
                <Box sx={{ mt: 3, display: 'flex', alignItems: 'center', color: 'error.main' }}>
                  <CloseIcon />
                  <Typography variant="h6" sx={{ ml: 1 }}>
                    Incorrect! The word was: {currentWord}
                  </Typography>
                </Box>
              )}
            </>
          )}
        </Paper>
        
        <Paper elevation={2} sx={{ p: 3 }}>
          <Typography variant="h5" gutterBottom>
            Difficulty Level
          </Typography>
          <Box sx={{ display: 'flex', justifyContent: 'space-between', mt: 2 }}>
            {['Easy', 'Medium', 'Hard'].map((level) => (
              <Button
                key={level}
                variant={difficulty === level ? 'contained' : 'outlined'}
                color="primary"
                onClick={() => handleDifficultyChange(level as 'Easy' | 'Medium' | 'Hard')}
                sx={{ width: '30%', py: 1.5 }}
              >
                {level}
              </Button>
            ))}
          </Box>
        </Paper>
      </Box>
    </Container>
  );
};

export default GamePage; 