/*
 * Licensed to the Apache Software Foundation (ASF) under one
 * or more contributor license agreements.  See the NOTICE file
 * distributed with this work for additional information
 * regarding copyright ownership.  The ASF licenses this file
 * to you under the Apache License, Version 2.0 (the
 * "License"); you may not use this file except in compliance
 * with the License.  You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing,
 * software distributed under the License is distributed on an
 * "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
 * KIND, either express or implied.  See the License for the
 * specific language governing permissions and limitations
 * under the License.
 */
import static org.mockito.Mockito.mock;
import static org.mockito.Mockito.when;
import com.example.pulsarworkshop.Order;
import com.example.pulsarworkshop.EmbeddingTransformFunction;
import java.util.List;
import org.apache.pulsar.functions.api.Context;
import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.Test;
import org.slf4j.Logger;

public class TestFunction {

    private List<Order> collection;

    @Test
    public void testOpenAI() throws Exception {
        var func = new EmbeddingTransformFunction();
        var orderMock = mock(Order.class);
        when(orderMock.getProductDescription()).thenReturn("test description");
        when(orderMock.getProductName()).thenReturn("example name");
        var contextMock = mock(Context.class);
        var loggerMock = mock(Logger.class);
        when(contextMock.getLogger()).thenReturn(loggerMock);
        func.initialize(contextMock);
        var newOrder = func.processLogic(orderMock, contextMock);
        Assertions.assertNotNull(newOrder.getEmbedding());
        Assertions.assertTrue(newOrder.getEmbedding().size() > 1);
    }
}