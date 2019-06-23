# convergence
#### A REStful API that helps you find the ideal place to meet.

Convergence is a RESTful API built using Flask and using the Google Maps API that helps groups of friends, colleagues, or acquiantances, find the ideal place to meet.

Users of Convergence can create groups and add others to these groups. Each user can specify whether or not they are "available" for the next get-together.  Convergence will suggest several suitable places, based on distance, travel times, and ratings, to meet with all those within your group who are keen to come.


#### Building Web Frontend

- Install node and npm with your package manager of choice.
- Navigate to the folder with all the frontend content:
```sh
cd convergence/static
```
- Install all dependencies with:
```sh
npm install
```
- When deploying to stage or production build distribution with:
```sh
npm run build-prod
```
- When debugging use:
```sh
npm run build-debug
```
- Or build and remain in watch mode with:
```sh
npm start
```
