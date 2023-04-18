# Use an official Nginx base image
FROM nginx:latest

# Remove the default Nginx configuration
RUN rm /etc/nginx/conf.d/default.conf

# Copy custom Nginx configuration
COPY nginx.conf /etc/nginx/

# Copy static files for the frontend
COPY frontend/ /usr/share/nginx/html/

# Start Nginx service
CMD ["nginx", "-g", "daemon off;"]
