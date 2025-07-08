# Use Node.js 18 as base image
FROM node:18-alpine

# Set working directory
WORKDIR /app

# Copy package files first (for better Docker layer caching)
COPY package*.json ./

# Install all dependencies (including dev dependencies)
RUN npm ci

# Copy source code
COPY . .

# Expose port 5173 (Vite's default dev port)
EXPOSE 5173

# Run the development server
CMD ["npm", "run", "dev", "--", "--host"] 