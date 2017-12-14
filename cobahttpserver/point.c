#include <GL/glut.h>
#include <stdlib.h>

static GLfloat spin = 0;

void display(void)
{
    glClear(GL_COLOR_BUFFER_BIT);
	//glPushMatrix();
	glRotatef(spin, 0.0, 0.0, 1.0);
	glColor3f(1.0, 1.0, 1.0);
	
	glBegin(GL_POINTS);
      glVertex3f (10 , 10, 0.0);
      glVertex3f (-10, 10, 0.0);
      glVertex3f (-10,-10, 0.0);	
      glVertex3f (10 ,-10, 0.0);
	glEnd();

	//glPopMatrix();
	glFlush();
}


void init(void) 
{
	glClearColor (0.0, 0.0, 0.0, 0.0);
	glOrtho(-50.0, 50.0, -50.0, 50.0, -1.0, 1.0);
}


void spe_key(char key, int x, int y) 
{
   
	switch (key) {

		case GLUT_KEY_LEFT:
			spin = 5;
			glutPostRedisplay();
			break;

		case GLUT_KEY_RIGHT:
			spin = -5;
			glutPostRedisplay();
			break;

	  default:
			break;
	}
}


/* 
 *
 *  Register mouse input callback functions
 */


int main()
{
	glutInitDisplayMode (GLUT_SINGLE | GLUT_RGB);
	glutInitWindowSize (250, 250); 
	glutInitWindowPosition (100, 100);
	glutCreateWindow ("mist");
	init();
	glutDisplayFunc(display);

	glutSpecialFunc(spe_key);

	glutMainLoop();
	return 0;   /* ANSI C requires main to return int. */
}

