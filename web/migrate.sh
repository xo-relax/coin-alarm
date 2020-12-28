if [ -d "./migrations" ]; then
  echo "migrations direcotry is already exists"
elif [ ! -d "./migrations" ]; then
  python manage.py db init; 
fi
python manage.py db migrate 
python manage.py db upgrade