require_relative 'rpc_client'

describe RpcClient do

  let(:connection) { Bunny.new(:automatically_recover => false) }

  let(:channel) { connection.start; connection.create_channel }

  let(:client) { RpcClient.new(channel, "rpc_queue") }

  it 'should calculate the fibonacci for a number' do
    expect(client.call(30)).to eq(832040)
  end

  after do
    channel.close
    connection.close
  end
end
