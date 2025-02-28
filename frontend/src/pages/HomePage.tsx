import React from 'react';
import { useNavigate } from 'react-router-dom';
import { 
  Container, 
  Typography, 
  Button, 
  Box, 
  Card, 
  CardContent,
  Grid,
  Paper
} from '@mui/material';
import { styled } from '@mui/material/styles';
import SoundIcon from '@mui/icons-material/GraphicEq';

const StyledCard = styled(Card)(({ theme }) => ({
  height: '100%',
  display: 'flex',
  flexDirection: 'column',
  transition: 'transform 0.3s ease-in-out',
  '&:hover': {
    transform: 'translateY(-8px)',
  },
}));

const SoundButton = styled(Button)(({ theme }) => ({
  margin: theme.spacing(1),
  padding: theme.spacing(2),
  minWidth: '120px',
}));

const HomePage: React.FC = () => {
  const navigate = useNavigate();
  
  const soundOptions = [
    { sound: 'th', examples: 'think, three, thumb' },
    { sound: 'sh', examples: 'ship, wish, shop' },
    { sound: 'ch', examples: 'chair, watch, church' },
    { sound: 'ph', examples: 'phone, graph, photo' },
    { sound: 'wh', examples: 'what, when, where' },
    { sound: 'ng', examples: 'sing, ring, king' },
  ];

  const handleSoundSelect = (sound: string) => {
    navigate('/game', { state: { focusSound: sound } });
  };

  return (
    <Container maxWidth="lg">
      <Box sx={{ my: 8, textAlign: 'center' }}>
        <Typography variant="h2" component="h1" gutterBottom>
          Word Sound Practice
        </Typography>
        <Typography variant="h5" color="textSecondary" paragraph>
          Improve your pronunciation by practicing specific sound patterns
        </Typography>
        
        <Paper elevation={0} sx={{ p: 4, mt: 4, backgroundColor: 'rgba(255,255,255,0.8)' }}>
          <Typography variant="h4" gutterBottom>
            Select a sound to practice:
          </Typography>
          
          <Grid container spacing={3} sx={{ mt: 2 }}>
            {soundOptions.map((option) => (
              <Grid item xs={12} sm={6} md={4} key={option.sound}>
                <StyledCard>
                  <CardContent>
                    <Box display="flex" alignItems="center" justifyContent="center" mb={2}>
                      <SoundIcon fontSize="large" color="primary" />
                      <Typography variant="h3" component="div" sx={{ ml: 1 }}>
                        "{option.sound}"
                      </Typography>
                    </Box>
                    <Typography color="textSecondary" gutterBottom>
                      Examples: {option.examples}
                    </Typography>
                    <Button 
                      variant="contained" 
                      color="primary" 
                      fullWidth 
                      size="large"
                      onClick={() => handleSoundSelect(option.sound)}
                      sx={{ mt: 2 }}
                    >
                      Practice
                    </Button>
                  </CardContent>
                </StyledCard>
              </Grid>
            ))}
          </Grid>
        </Paper>
      </Box>
    </Container>
  );
};

export default HomePage; 