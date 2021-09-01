#define F_CPU 16000000UL // Defining the CPU Frequency

#include <avr/io.h>      // Contains all the I/O Register Macros

#define USART_BAUDRATE 9600         // Desired Baud Rate
#define BAUD_PRESCALER (((F_CPU / (USART_BAUDRATE * 16UL))) - 1)
#define ASYNCHRONOUS   (0<<UMSEL00) // USART Mode Selection
#define PARITY_MODE    (0<<UPM00)   // USART Parity Bit Selection
#define STOP_BIT       (0<<USBS0)   // USART Stop Bit Selection
#define DATA_BIT       (3<<UCSZ00)  // USART Data Bit Selection

#define MOTOR_ENABLE_PIN
#define MOTORA_STEP_PIN 2
#define MOTORB_STEP_PIN 3
#define MOTORC_STEP_PIN 4
#define MOTORA_DIR_PIN  5 
#define MOTORB_DIR_PIN  6
#define MOTORC_DIR_PIN  7

typedef struct
{
  int  stepperPin = 0;   // This will get set for each motor in PORT_init()
  int  pulseTicks = 200; // How many ticks to run for next step to begin
  int  tickCount = 0;    // How many ticks since last step ended
  int  pulseLength = 10; // How many ticks the stepperPin will be held HIGH
  int  currentSpeed = 0; //
  int  targetSpeed = 0;  //
  int  traveled = 0;     // How many steps the motor has traveled since last UART transmit
  bool stepping = false; // True if motor is being stepped, false otherwise
}m;

volatile m motorA;

boolean receiving = false;
int recv_pos = 0;
char recv_buffer[16];
char erOverrun[] = "Buffer Overrun!";
uint8_t DataByte;



int main(void)
{
  SYS_init();

  while (1)
  {
    if (( UCSR0A & (1<<RXC0)))
    {
      DataByte = UDR0;
      if (receiving)
      {
        if (DataByte == '\n')
        {
          sendmsg(recv_buffer, recv_pos);
          motorA.currentSpeed = atoi(recv_buffer);
          motorA.pulseTicks = 200000 / motorA.currentSpeed;
          receiving = false;
        }
        else
        {
          if (recv_pos < 16)
          {
            recv_buffer[recv_pos] = DataByte;
            recv_pos++;
          }
          else
          {
            sendmsg(erOverrun, 16);
            receiving = false;
          }
        }
      }          
      else
      {
        if (DataByte == 'A')
        {
          recv_pos = 0;
          memset(recv_buffer, 0, 16);
          receiving = true;
        }
      }
    }
  }
  return 0;
}

ISR(TIMER1_COMPA_vect)
{
  updateMotor(&motorA, MOTORA_STEP_PIN, MOTORA_DIR_PIN);
}

void updateMotor(m *motor, int stepPin, int dirPin)
{
  motor->tickCount++;
  if (motor->stepping)
  {
    if (motor->tickCount >= motor->pulseLength)
    {
      PORTD &= ~(1 << stepPin);
      motor->stepping = false;
    }
  }
  else
  {
    if (motor->tickCount >= motor->pulseTicks)
    {
      if (motor->currentSpeed > 0){PORTD |= 1 << dirPin;}
      else {PORTD &= ~(1 << dirPin);}
      PORTD |= 1 << stepPin;
      motor->stepping = true;
      motor->tickCount = 0;
    }
  }
}

void SYS_init()
{
  DDRD |= B11111100;  // set pins 2 thru 7 as outputs
  pinMode(8, OUTPUT);
  digitalWrite(8, LOW);
  cli();              // disable interrupts
  TIMER1_init();      // initialize TIMER_1 with interrupt
  USART_init();       // initialize serial communication
  sei();              // enable interrupts
}

void TIMER1_init()
{
  TCCR1A = 0;                          // set entire TCCR1A register to 0
  TCCR1B = 0;                          // same for TCCR1B
  TCNT1  = 0;                          // initialize counter value
  OCR1A = 9;                           // set compare match register for 200kHz
  TCCR1B |= (1 << WGM12);              // turn on CTC mode
  TCCR1B |= (1 << CS11);               // Set CS11 bit for 8 prescaler
  TIMSK1 |= (1 << OCIE1A);             // enable timer compare interrupt
}

void USART_init()
{
  // Set Baud Rate
  UBRR0H = BAUD_PRESCALER >> 8;
  UBRR0L = BAUD_PRESCALER;
  
  // Set Frame Format
  UCSR0C = ASYNCHRONOUS | PARITY_MODE | STOP_BIT | DATA_BIT;
  
  // Enable Receiver and Transmitter
  UCSR0B = (1<<RXEN0) | (1<<TXEN0);
}

void sendmsg(byte *data, int recv_size)
{
  for (int i = 0; i < recv_size; i++)
  {
     USART_TransmitPolling(data[i]);
  }
  USART_TransmitPolling('\n');
}

void USART_TransmitPolling(uint8_t DataByte)
{
  while (( UCSR0A & (1<<UDRE0)) == 0) {}; // Do nothing until UDR is ready
  UDR0 = DataByte;
}
