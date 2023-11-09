#include <SFML/Graphics.hpp>
#include <time.h>
#include <SFML/Audio.hpp>
#include <iostream>

using namespace sf;

const int M = 20; //Altura de la matriz
const int N = 10; //Ancho de la matriz

int score = 0;
int level = 1;

int field[M][N] = {0};

struct Point
{int x,y;} a[4], b[4];

int figures[7][4] =
{
    1,3,5,7, // I
    2,4,5,7, // Z
    3,5,4,6, // S
    3,5,4,7, // T
    2,3,5,7, // L
    3,5,7,6, // J
    2,3,4,5, // O
};
Font font;
Text gameOverText;

bool check()
{
   for (int i=0;i<4;i++)
      if (a[i].x<0 || a[i].x>=N || a[i].y>=M) return 0;
      else if (field[a[i].y][a[i].x]) return 0;

   return 1;
};

//funcion game over
bool gameOver() {
    for (int j = 0; j <= N; j++) {
        if (field[0][j]) { // Si hay un bloque en la fila superior
            return true;
        }
    }
    return false;
}





int main()
{
    srand(time(0));     

    RenderWindow window(VideoMode(320, 480), "TETRIS auspiciado por BCP");

    Texture t1,t2;
    t1.loadFromFile("images/tiles.png");
    t2.loadFromFile("images/background.png");
    //agragando
   //Contexto

    Sprite s(t1), background(t2);

    int dx=0; bool rotate=0; int colorNum=1;
    float timer=0,delay=.3; 

    Clock clock;
    
    
    sf::Music music;
    if (!music.openFromFile("musica/music.ogg")) {
    // Maneja el error si no puedes cargar la música.
    std::cerr << "Error al cargar la música!" << std::endl;
    }
	music.setLoop(true); // Esto hará que la música se repita.
	music.play();

    
    
    // GAME OVER
    
    
    
    
    
    

    while (window.isOpen())
    {
        float time = clock.getElapsedTime().asSeconds();
        clock.restart();
        timer+=time;

        Event e;
        while (window.pollEvent(e))
        {
            if (e.type == Event::Closed)
                window.close();

            if (e.type == Event::KeyPressed)
              if (e.key.code==Keyboard::Up) rotate=true;
              else if (e.key.code==Keyboard::Left) dx=-1;
              else if (e.key.code==Keyboard::Right) dx=1;
        }

    if (Keyboard::isKeyPressed(Keyboard::Down)) delay=0.05;

    //// <- Movimiento -> ///
    for (int i=0;i<4;i++)  { b[i]=a[i]; a[i].x+=dx; }
    if (!check()) for (int i=0;i<4;i++) a[i]=b[i];

    //////Rotacion//////
    if (rotate)
      {
        Point p = a[1]; //center of rotation
        for (int i=0;i<4;i++)
          {
            int x = a[i].y-p.y;
            int y = a[i].x-p.x;
            a[i].x = p.x - x;
            a[i].y = p.y + y;
           }
           if (!check()) for (int i=0;i<4;i++) a[i]=b[i];
      }

    ///////Tick//////
    if (timer>delay)
      {
        for (int i=0;i<4;i++) { b[i]=a[i]; a[i].y+=1; }


// agregando cambio
        if (!check())
{
    for (int i = 0; i < 4; i++) field[b[i].y][b[i].x] = colorNum;

    if (gameOver()) { // Verificar si el jugador ha perdido
        window.close(); // Cerrar la ventana para terminar el juego
        return 0; // Terminar el programa
    }

    colorNum = 1 + rand() % 7;
    int n = rand() % 7;
    for (int i = 0; i < 4; i++)
    {
        a[i].x = figures[n][i] % 2;
        a[i].y = figures[n][i] / 2;
    }
}


		//cambio de game over
         timer=0;
      }

    ///////Verificar lineas//////////
    int k = M - 1;
int lines = 0; // Para contar las líneas completadas en un turno
for (int i = M - 1; i > 0; i--)
    {
        int count=0;
        for (int j=0;j<N;j++)
        {
            if (field[i][j]) count++;
            field[k][j]=field[i][j];
        }
        if (count<N) k--;
    }

    dx=0; rotate=0; delay=0.3;
    
    
    
    
    

    /////////draw//////////
    window.clear(Color::White);    
    window.draw(background);
          
    for (int i=0;i<M;i++)
     for (int j=0;j<N;j++)
       {
         if (field[i][j]==0) continue;
         s.setTextureRect(IntRect(field[i][j]*18,0,18,18));
         s.setPosition(j*18,i*18);
         s.move(28,31); //offset
         window.draw(s);
       }

    for (int i=0;i<4;i++)
      {
        s.setTextureRect(IntRect(colorNum*18,0,18,18));
        s.setPosition(a[i].x*18,a[i].y*18);
        s.move(28,31); //offset
        window.draw(s);
      }

    
    window.display();
    }

    return 0;
}
