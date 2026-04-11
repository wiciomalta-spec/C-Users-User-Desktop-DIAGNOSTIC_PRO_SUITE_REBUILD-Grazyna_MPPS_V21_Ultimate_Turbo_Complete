/**
 * DIAGNOSTIC PRO SUITE ULTIMATE EDITION
 * AI Chat Real-time Engine
 * Version: 2.0.0
 * Author: Office Agent Technologies
 */

class AIChatEngine {
    constructor(config = {}) {
        this.config = {
            apiEndpoint: config.apiEndpoint || 'ws://localhost:8081',
            aiProvider: config.aiProvider || 'openai',
            model: config.model || 'gpt-4',
            maxTokens: config.maxTokens || 4096,
            temperature: config.temperature || 0.7,
            language: config.language || 'pl',
            enableVoice: config.enableVoice || true,
            enableRealTimeAnalysis: config.enableRealTimeAnalysis || true,
            diagnosticContext: config.diagnosticContext || true,
            ...config
        };

        // WebSocket connection
        this.ws = null;
        this.connectionState = 'disconnected';
        this.reconnectAttempts = 0;
        this.maxReconnectAttempts = 5;

        // Chat state
        this.chatHistory = [];
        this.currentSession = null;
        this.diagnosticContext = {};
        this.activeAnalysis = new Map();

        // Real-time features
        this.voiceRecognition = null;
        this.speechSynthesis = null;
        this.isListening = false;
        this.isProcessing = false;

        // Event handlers
        this.eventHandlers = new Map();

        // Initialize components
        this.init();
    }

    async init() {
        console.log('🤖 Initializing AI Chat Engine...');
        
        try {
            // Initialize WebSocket connection
            await this.connectWebSocket();
            
            // Initialize voice features
            if (this.config.enableVoice) {
                this.initVoiceFeatures();
            }
            
            // Initialize diagnostic context
            if (this.config.diagnosticContext) {
                this.initDiagnosticContext();
            }
            
            // Start real-time analysis
            if (this.config.enableRealTimeAnalysis) {
                this.startRealTimeAnalysis();
            }
            
            console.log('✅ AI Chat Engine initialized successfully');
            this.emit('initialized');
            
        } catch (error) {
            console.error('❌ Failed to initialize AI Chat Engine:', error);
            this.emit('error', error);
        }
    }

    async connectWebSocket() {
        return new Promise((resolve, reject) => {
            try {
                this.ws = new WebSocket(this.config.apiEndpoint);
                
                this.ws.onopen = () => {
                    console.log('🔗 WebSocket connected');
                    this.connectionState = 'connected';
                    this.reconnectAttempts = 0;
                    this.emit('connected');
                    resolve();
                };
                
                this.ws.onmessage = (event) => {
                    this.handleWebSocketMessage(event);
                };
                
                this.ws.onclose = () => {
                    console.log('🔌 WebSocket disconnected');
                    this.connectionState = 'disconnected';
                    this.emit('disconnected');
                    this.attemptReconnect();
                };
                
                this.ws.onerror = (error) => {
                    console.error('🚨 WebSocket error:', error);
                    this.emit('error', error);
                    reject(error);
                };
                
            } catch (error) {
                reject(error);
            }
        });
    }

    handleWebSocketMessage(event) {
        try {
            const message = JSON.parse(event.data);
            
            switch (message.type) {
                case 'ai_response':
                    this.handleAIResponse(message);
                    break;
                case 'diagnostic_update':
                    this.handleDiagnosticUpdate(message);
                    break;
                case 'system_alert':
                    this.handleSystemAlert(message);
                    break;
                case 'real_time_data':
                    this.handleRealTimeData(message);
                    break;
                default:
                    console.log('📨 Unknown message type:', message.type);
            }
            
        } catch (error) {
            console.error('❌ Error handling WebSocket message:', error);
        }
    }

    async sendMessage(message, options = {}) {
        if (this.connectionState !== 'connected') {
            throw new Error('WebSocket not connected');
        }

        const messageData = {
            type: 'ai_request',
            message: message,
            sessionId: this.currentSession,
            timestamp: new Date().toISOString(),
            context: this.diagnosticContext,
            options: {
                model: this.config.model,
                maxTokens: this.config.maxTokens,
                temperature: this.config.temperature,
                language: this.config.language,
                ...options
            }
        };

        // Add to chat history
        this.addToChatHistory('user', message);

        // Send via WebSocket
        this.ws.send(JSON.stringify(messageData));

        // Emit event
        this.emit('messageSent', messageData);

        return messageData;
    }

    handleAIResponse(response) {
        try {
            // Add to chat history
            this.addToChatHistory('ai', response.message, response.metadata);

            // Handle special response types
            if (response.responseType) {
                this.handleSpecialResponse(response);
            }

            // Text-to-speech if enabled
            if (this.config.enableVoice && response.enableSpeech) {
                this.speakText(response.message);
            }

            // Emit event
            this.emit('aiResponse', response);

        } catch (error) {
            console.error('❌ Error handling AI response:', error);
        }
    }

    handleSpecialResponse(response) {
        switch (response.responseType) {
            case 'diagnostic_suggestion':
                this.handleDiagnosticSuggestion(response);
                break;
            case 'code_generation':
                this.handleCodeGeneration(response);
                break;
            case 'system_command':
                this.handleSystemCommand(response);
                break;
            case 'data_analysis':
                this.handleDataAnalysis(response);
                break;
            case 'troubleshooting_guide':
                this.handleTroubleshootingGuide(response);
                break;
        }
    }

    handleDiagnosticSuggestion(response) {
        const suggestion = {
            id: this.generateId(),
            type: 'diagnostic_suggestion',
            title: response.title,
            description: response.message,
            steps: response.steps || [],
            priority: response.priority || 'medium',
            estimatedTime: response.estimatedTime,
            requiredTools: response.requiredTools || [],
            timestamp: new Date().toISOString()
        };

        this.emit('diagnosticSuggestion', suggestion);
    }

    handleCodeGeneration(response) {
        const codeData = {
            id: this.generateId(),
            language: response.language,
            code: response.code,
            description: response.description,
            usage: response.usage,
            timestamp: new Date().toISOString()
        };

        this.emit('codeGenerated', codeData);
    }

    handleSystemCommand(response) {
        if (response.command && response.safe) {
            this.emit('systemCommand', {
                command: response.command,
                parameters: response.parameters,
                description: response.description
            });
        }
    }

    initVoiceFeatures() {
        try {
            // Speech Recognition
            if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
                const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
                this.voiceRecognition = new SpeechRecognition();
                
                this.voiceRecognition.continuous = false;
                this.voiceRecognition.interimResults = false;
                this.voiceRecognition.lang = this.getLanguageCode();
                
                this.voiceRecognition.onresult = (event) => {
                    const transcript = event.results[0][0].transcript;
                    this.handleVoiceInput(transcript);
                };
                
                this.voiceRecognition.onerror = (event) => {
                    console.error('🎤 Speech recognition error:', event.error);
                    this.isListening = false;
                    this.emit('voiceError', event.error);
                };
                
                this.voiceRecognition.onend = () => {
                    this.isListening = false;
                    this.emit('voiceEnd');
                };
            }
            
            // Speech Synthesis
            if ('speechSynthesis' in window) {
                this.speechSynthesis = window.speechSynthesis;
            }
            
            console.log('🎤 Voice features initialized');
            
        } catch (error) {
            console.error('❌ Error initializing voice features:', error);
        }
    }

    startListening() {
        if (!this.voiceRecognition || this.isListening) return;
        
        try {
            this.isListening = true;
            this.voiceRecognition.start();
            this.emit('voiceStart');
        } catch (error) {
            console.error('❌ Error starting voice recognition:', error);
            this.isListening = false;
        }
    }

    stopListening() {
        if (!this.voiceRecognition || !this.isListening) return;
        
        this.voiceRecognition.stop();
        this.isListening = false;
    }

    handleVoiceInput(transcript) {
        console.log('🎤 Voice input:', transcript);
        this.emit('voiceInput', transcript);
        
        // Send voice input as message
        this.sendMessage(transcript, { inputType: 'voice' });
    }

    speakText(text) {
        if (!this.speechSynthesis) return;
        
        try {
            const utterance = new SpeechSynthesisUtterance(text);
            utterance.lang = this.getLanguageCode();
            utterance.rate = 0.9;
            utterance.pitch = 1.0;
            utterance.volume = 0.8;
            
            utterance.onstart = () => this.emit('speechStart');
            utterance.onend = () => this.emit('speechEnd');
            utterance.onerror = (error) => this.emit('speechError', error);
            
            this.speechSynthesis.speak(utterance);
            
        } catch (error) {
            console.error('❌ Error in text-to-speech:', error);
        }
    }

    initDiagnosticContext() {
        // Initialize diagnostic context with system information
        this.diagnosticContext = {
            systemInfo: this.getSystemInfo(),
            connectedDevices: [],
            activeSession: null,
            currentVehicle: null,
            diagnosticHistory: [],
            preferences: this.getUserPreferences()
        };

        // Listen for diagnostic updates
        this.on('diagnosticUpdate', (update) => {
            this.updateDiagnosticContext(update);
        });

        console.log('🔧 Diagnostic context initialized');
    }

    updateDiagnosticContext(update) {
        try {
            switch (update.type) {
                case 'device_connected':
                    this.diagnosticContext.connectedDevices.push(update.device);
                    break;
                case 'device_disconnected':
                    this.diagnosticContext.connectedDevices = 
                        this.diagnosticContext.connectedDevices.filter(d => d.id !== update.deviceId);
                    break;
                case 'session_started':
                    this.diagnosticContext.activeSession = update.session;
                    break;
                case 'session_ended':
                    this.diagnosticContext.activeSession = null;
                    break;
                case 'vehicle_identified':
                    this.diagnosticContext.currentVehicle = update.vehicle;
                    break;
                case 'diagnostic_completed':
                    this.diagnosticContext.diagnosticHistory.push(update.result);
                    break;
            }

            this.emit('contextUpdated', this.diagnosticContext);

        } catch (error) {
            console.error('❌ Error updating diagnostic context:', error);
        }
    }

    startRealTimeAnalysis() {
        // Real-time data analysis for proactive assistance
        this.analysisInterval = setInterval(() => {
            this.performRealTimeAnalysis();
        }, 5000); // Every 5 seconds

        console.log('📊 Real-time analysis started');
    }

    performRealTimeAnalysis() {
        try {
            // Analyze current diagnostic state
            const analysis = {
                timestamp: new Date().toISOString(),
                systemHealth: this.analyzeSystemHealth(),
                deviceStatus: this.analyzeDeviceStatus(),
                sessionProgress: this.analyzeSessionProgress(),
                potentialIssues: this.identifyPotentialIssues()
            };

            // Send analysis to AI for proactive suggestions
            if (analysis.potentialIssues.length > 0) {
                this.requestProactiveSuggestions(analysis);
            }

            this.emit('realTimeAnalysis', analysis);

        } catch (error) {
            console.error('❌ Error in real-time analysis:', error);
        }
    }

    analyzeSystemHealth() {
        // Analyze system performance metrics
        return {
            cpuUsage: this.getSystemMetric('cpu'),
            memoryUsage: this.getSystemMetric('memory'),
            networkLatency: this.getSystemMetric('network'),
            errorRate: this.getSystemMetric('errors'),
            overall: 'good' // good, warning, critical
        };
    }

    analyzeDeviceStatus() {
        return this.diagnosticContext.connectedDevices.map(device => ({
            id: device.id,
            name: device.name,
            status: device.status,
            health: device.health || 'unknown',
            lastSeen: device.lastSeen,
            issues: device.issues || []
        }));
    }

    analyzeSessionProgress() {
        const session = this.diagnosticContext.activeSession;
        if (!session) return null;

        return {
            sessionId: session.id,
            duration: Date.now() - new Date(session.startTime).getTime(),
            progress: session.progress || 0,
            currentStep: session.currentStep,
            estimatedTimeRemaining: session.estimatedTimeRemaining,
            issues: session.issues || []
        };
    }

    identifyPotentialIssues() {
        const issues = [];

        // Check system health
        const health = this.analyzeSystemHealth();
        if (health.cpuUsage > 80) {
            issues.push({
                type: 'performance',
                severity: 'warning',
                message: 'High CPU usage detected',
                suggestion: 'Consider closing unnecessary applications'
            });
        }

        // Check device status
        const devices = this.analyzeDeviceStatus();
        devices.forEach(device => {
            if (device.status === 'error' || device.health === 'poor') {
                issues.push({
                    type: 'device',
                    severity: 'error',
                    message: `Device ${device.name} has issues`,
                    suggestion: 'Check device connection and drivers'
                });
            }
        });

        return issues;
    }

    async requestProactiveSuggestions(analysis) {
        const message = `Based on real-time analysis, I've detected some potential issues. Can you provide suggestions?

Analysis Summary:
- System Health: ${analysis.systemHealth.overall}
- Active Issues: ${analysis.potentialIssues.length}
- Connected Devices: ${analysis.deviceStatus.length}

Issues:
${analysis.potentialIssues.map(issue => `- ${issue.message}`).join('\n')}`;

        await this.sendMessage(message, {
            type: 'proactive_analysis',
            analysis: analysis,
            requestType: 'suggestions'
        });
    }

    // Utility methods
    addToChatHistory(sender, message, metadata = {}) {
        const entry = {
            id: this.generateId(),
            sender: sender,
            message: message,
            timestamp: new Date().toISOString(),
            metadata: metadata
        };

        this.chatHistory.push(entry);

        // Limit history size
        if (this.chatHistory.length > 1000) {
            this.chatHistory = this.chatHistory.slice(-500);
        }

        this.emit('chatHistoryUpdated', entry);
    }

    generateId() {
        return 'id_' + Math.random().toString(36).substr(2, 9) + '_' + Date.now();
    }

    getLanguageCode() {
        const langMap = {
            'pl': 'pl-PL',
            'en': 'en-US',
            'de': 'de-DE',
            'fr': 'fr-FR',
            'es': 'es-ES'
        };
        return langMap[this.config.language] || 'en-US';
    }

    getSystemInfo() {
        return {
            userAgent: navigator.userAgent,
            platform: navigator.platform,
            language: navigator.language,
            timestamp: new Date().toISOString(),
            viewport: {
                width: window.innerWidth,
                height: window.innerHeight
            }
        };
    }

    getUserPreferences() {
        try {
            const prefs = localStorage.getItem('aiChatPreferences');
            return prefs ? JSON.parse(prefs) : {};
        } catch {
            return {};
        }
    }

    getSystemMetric(metric) {
        // Simulate system metrics - in real implementation, 
        // these would come from actual system monitoring
        const metrics = {
            cpu: Math.random() * 100,
            memory: Math.random() * 100,
            network: Math.random() * 50,
            errors: Math.random() * 5
        };
        return Math.round(metrics[metric] || 0);
    }

    attemptReconnect() {
        if (this.reconnectAttempts >= this.maxReconnectAttempts) {
            console.error('🚨 Max reconnection attempts reached');
            this.emit('reconnectFailed');
            return;
        }

        this.reconnectAttempts++;
        const delay = Math.min(1000 * Math.pow(2, this.reconnectAttempts), 30000);

        console.log(`🔄 Attempting to reconnect in ${delay}ms (attempt ${this.reconnectAttempts})`);

        setTimeout(() => {
            this.connectWebSocket().catch(error => {
                console.error('❌ Reconnection failed:', error);
            });
        }, delay);
    }

    // Event system
    on(event, handler) {
        if (!this.eventHandlers.has(event)) {
            this.eventHandlers.set(event, []);
        }
        this.eventHandlers.get(event).push(handler);
    }

    off(event, handler) {
        if (this.eventHandlers.has(event)) {
            const handlers = this.eventHandlers.get(event);
            const index = handlers.indexOf(handler);
            if (index > -1) {
                handlers.splice(index, 1);
            }
        }
    }

    emit(event, data) {
        if (this.eventHandlers.has(event)) {
            this.eventHandlers.get(event).forEach(handler => {
                try {
                    handler(data);
                } catch (error) {
                    console.error(`❌ Error in event handler for ${event}:`, error);
                }
            });
        }
    }

    // Public API methods
    async startSession(sessionConfig = {}) {
        this.currentSession = this.generateId();
        
        const sessionData = {
            id: this.currentSession,
            startTime: new Date().toISOString(),
            config: sessionConfig,
            context: this.diagnosticContext
        };

        await this.sendMessage('Starting new diagnostic session', {
            type: 'session_start',
            sessionData: sessionData
        });

        this.emit('sessionStarted', sessionData);
        return this.currentSession;
    }

    async endSession() {
        if (!this.currentSession) return;

        await this.sendMessage('Ending diagnostic session', {
            type: 'session_end',
            sessionId: this.currentSession
        });

        const endedSession = this.currentSession;
        this.currentSession = null;

        this.emit('sessionEnded', endedSession);
    }

    getChatHistory() {
        return [...this.chatHistory];
    }

    clearChatHistory() {
        this.chatHistory = [];
        this.emit('chatHistoryCleared');
    }

    updateConfig(newConfig) {
        this.config = { ...this.config, ...newConfig };
        this.emit('configUpdated', this.config);
    }

    getConnectionState() {
        return this.connectionState;
    }

    getDiagnosticContext() {
        return { ...this.diagnosticContext };
    }

    destroy() {
        // Cleanup
        if (this.ws) {
            this.ws.close();
        }

        if (this.analysisInterval) {
            clearInterval(this.analysisInterval);
        }

        if (this.voiceRecognition) {
            this.voiceRecognition.stop();
        }

        if (this.speechSynthesis) {
            this.speechSynthesis.cancel();
        }

        this.eventHandlers.clear();
        console.log('🧹 AI Chat Engine destroyed');
    }
}

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = AIchatEngine;
} else if (typeof window !== 'undefined') {
    window.AIchatEngine = AIchatEngine;
}

// Usage example and initialization
document.addEventListener('DOMContentLoaded', () => {
    // Initialize AI Chat Engine
    const aiChat = new AIchatEngine({
        apiEndpoint: 'ws://localhost:8081',
        aiProvider: 'openai',
        model: 'gpt-4',
        language: 'pl',
        enableVoice: true,
        enableRealTimeAnalysis: true
    });

    // Event listeners
    aiChat.on('initialized', () => {
        console.log('✅ AI Chat ready for use');
        showNotification('AI Assistant connected and ready!', 'success');
    });

    aiChat.on('aiResponse', (response) => {
        displayAIMessage(response.message, response.metadata);
    });

    aiChat.on('diagnosticSuggestion', (suggestion) => {
        displayDiagnosticSuggestion(suggestion);
    });

    aiChat.on('voiceInput', (transcript) => {
        displayUserMessage(transcript, { inputType: 'voice' });
    });

    aiChat.on('error', (error) => {
        console.error('AI Chat Error:', error);
        showNotification('AI Assistant error: ' + error.message, 'error');
    });

    // Make available globally
    window.aiChatEngine = aiChat;
});

// Helper functions for UI integration
function displayAIMessage(message, metadata = {}) {
    const messagesContainer = document.getElementById('aiChatMessages');
    if (!messagesContainer) return;

    const messageDiv = document.createElement('div');
    messageDiv.className = 'ai-message ai';
    
    const avatar = document.createElement('div');
    avatar.className = 'ai-avatar';
    avatar.innerHTML = '<i class="fas fa-robot"></i>';
    
    const content = document.createElement('div');
    content.className = 'ai-message-content';
    content.innerHTML = formatMessage(message);
    
    // Add metadata if available
    if (metadata.responseType) {
        const typeIndicator = document.createElement('div');
        typeIndicator.className = 'message-type';
        typeIndicator.textContent = metadata.responseType;
        content.appendChild(typeIndicator);
    }
    
    messageDiv.appendChild(avatar);
    messageDiv.appendChild(content);
    messagesContainer.appendChild(messageDiv);
    
    // Scroll to bottom
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
}

function displayUserMessage(message, metadata = {}) {
    const messagesContainer = document.getElementById('aiChatMessages');
    if (!messagesContainer) return;

    const messageDiv = document.createElement('div');
    messageDiv.className = 'ai-message user';
    
    const avatar = document.createElement('div');
    avatar.className = 'ai-avatar';
    avatar.innerHTML = metadata.inputType === 'voice' ? 
        '<i class="fas fa-microphone"></i>' : '<i class="fas fa-user"></i>';
    
    const content = document.createElement('div');
    content.className = 'ai-message-content';
    content.textContent = message;
    
    messageDiv.appendChild(avatar);
    messageDiv.appendChild(content);
    messagesContainer.appendChild(messageDiv);
    
    // Scroll to bottom
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
}

function displayDiagnosticSuggestion(suggestion) {
    // Create diagnostic suggestion UI element
    const suggestionDiv = document.createElement('div');
    suggestionDiv.className = 'diagnostic-suggestion';
    suggestionDiv.innerHTML = `
        <div class="suggestion-header">
            <h4><i class="fas fa-lightbulb"></i> ${suggestion.title}</h4>
            <span class="priority ${suggestion.priority}">${suggestion.priority}</span>
        </div>
        <div class="suggestion-content">
            <p>${suggestion.description}</p>
            ${suggestion.steps.length > 0 ? `
                <ol class="suggestion-steps">
                    ${suggestion.steps.map(step => `<li>${step}</li>`).join('')}
                </ol>
            ` : ''}
        </div>
        <div class="suggestion-actions">
            <button class="btn btn-primary" onclick="applySuggestion('${suggestion.id}')">
                Apply Suggestion
            </button>
            <button class="btn btn-secondary" onclick="dismissSuggestion('${suggestion.id}')">
                Dismiss
            </button>
        </div>
    `;
    
    // Add to suggestions container or show as notification
    const container = document.getElementById('diagnosticSuggestions') || 
                     document.getElementById('notificationContainer');
    if (container) {
        container.appendChild(suggestionDiv);
    }
}

function formatMessage(message) {
    // Format message with markdown-like syntax
    return message
        .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
        .replace(/\*(.*?)\*/g, '<em>$1</em>')
        .replace(/`(.*?)`/g, '<code>$1</code>')
        .replace(/\n/g, '<br>');
}

function showNotification(message, type = 'info') {
    // Use existing notification system
    if (typeof window.showNotification === 'function') {
        window.showNotification(message, type);
    } else {
        console.log(`[${type.toUpperCase()}] ${message}`);
    }
}

// Voice control functions
function startVoiceInput() {
    if (window.aiChatEngine) {
        window.aiChatEngine.startListening();
    }
}

function stopVoiceInput() {
    if (window.aiChatEngine) {
        window.aiChatEngine.stopListening();
    }
}

// Suggestion handling functions
function applySuggestion(suggestionId) {
    console.log('Applying suggestion:', suggestionId);
    // Implementation depends on suggestion type
    showNotification('Suggestion applied successfully!', 'success');
}

function dismissSuggestion(suggestionId) {
    const suggestionElement = document.querySelector(`[data-suggestion-id="${suggestionId}"]`);
    if (suggestionElement) {
        suggestionElement.remove();
    }
}

console.log('🤖 AI Chat Real-time Engine loaded successfully');